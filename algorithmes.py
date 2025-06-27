import os
import re
import glob
import networkx as nx
import json


class AlgorithmesPriorite:
    def __init__(self, instance_data):
        self.data = instance_data
        self.activities = list(range(1, self.data['nActs'] + 1))
        self.durations = self.data['dur']
        self.precedence_graph = self.data['precedence_graph']
        self.est = self.data.get('est', [0]*self.data['nActs'])
        self.lst = self.data.get('lst', [0]*self.data['nActs'])
        self.lft = self.data.get('lft', [0]*self.data['nActs'])
        self.float_dyn = self.data.get(
            'float_dyn', [float('inf')] * self.data['nActs']
        )
        self.resource_usage = self.data.get('resource_usage', {})

        self.hrpw_memo = {}
        self.compute_successors()
        self.compute_hrpw_all()

    def compute_successors(self):
        for t in self.activities:
            if t not in self.precedence_graph:
                self.precedence_graph[t] = {
                    'successors': [],
                    'predecessors': []
                }

    def compute_hrpw(self, task):
        if task in self.hrpw_memo:
            return self.hrpw_memo[task]
        succ = self.precedence_graph[task]['successors']
        if not succ:
            val = self.durations[task-1]
        else:
            val = (
                self.durations[task-1]
                + max(self.compute_hrpw(s) for s in succ)
            )
        self.hrpw_memo[task] = val
        return val

    def compute_hrpw_all(self):
        for t in self.activities:
            self.compute_hrpw(t)

    def sort_by_hrpw(self):
        return sorted(
            self.activities,
            key=lambda t: self.hrpw_memo[t], reverse=True
        )

    def sort_by_lst(self):
        return sorted(self.activities, key=lambda t: self.lst[t-1])

    def sort_by_lft(self):
        return sorted(self.activities, key=lambda t: self.lft[t-1])

    def sort_by_mts(self):
        def count_successors(task):
            succ = self.precedence_graph[task]['successors']
            total = len(succ)
            for s in succ:
                total += count_successors(s)
            return total
        mts = {t: count_successors(t) for t in self.activities}
        return sorted(self.activities, key=lambda t: mts[t], reverse=True)

    def sort_by_timros(self):
        ratios = {}
        for t in self.activities:
            dur = self.durations[t-1]
            res = self.resource_usage.get(t, 1)
            ratios[t] = dur / res if res else float('inf')
        return sorted(self.activities, key=lambda t: ratios[t])

    def sort_by_hru1(self):
        usage = self.resource_usage
        return sorted(
            self.activities,
            key=lambda t: usage.get(t, 0),
            reverse=True
        )

    def sort_by_timres(self):
        scores = {}
        for t in self.activities:
            dur = self.durations[t-1]
            res = self.resource_usage.get(t, 1)
            scores[t] = dur * res
        return sorted(self.activities, key=lambda t: scores[t])

    def sort_by_hru2(self):
        usage = self.resource_usage
        return sorted(
            self.activities,
            key=lambda t: usage.get(t, 0)*self.durations[t-1],
            reverse=True
        )

    def sort_by_stfd(self):
        return sorted(
            self.activities,
            key=lambda t: self.float_dyn[t-1]
        )

    def sort_by_eft(self):
        eft = {t: self.est[t-1] + self.durations[t-1] for t in self.activities}
        return sorted(self.activities, key=lambda t: eft[t])

    def _respect_precedence(self, ordered_activities):
        G = nx.DiGraph()
        for a in self.activities:
            G.add_node(a)
        for a in self.activities:
            for s in self.precedence_graph[a]['successors']:
                G.add_edge(a, s)

        priority = {act: idx for idx, act in enumerate(ordered_activities)}
        try:
            remaining = set(ordered_activities)
            result = []
            while remaining:
                ready = [a for a in remaining if all(
                    pred not in remaining for pred in G.predecessors(a))]
                if not ready:
                    break
                next_act = min(
                    ready, key=lambda a: priority.get(a, float('inf')))
                result.append(next_act)
                remaining.remove(next_act)
            return result + list(remaining)
        except nx.NetworkXUnfeasible:
            print(
                "Cycle détecté dans le graphe, "
                "impossible de respecter précédence"
            )
            return ordered_activities

    def get_ordered_activities(self, rule_abbr):
        rule_map = {
            'HRPW*': self.sort_by_hrpw,
            'LST': self.sort_by_lst,
            'LFT': self.sort_by_lft,
            'MTS': self.sort_by_mts,
            'TIMROS': self.sort_by_timros,
            'HRU1': self.sort_by_hru1,
            'TIMRES': self.sort_by_timres,
            'HRU2': self.sort_by_hru2,
            'STFD': self.sort_by_stfd,
            'EFT': self.sort_by_eft
        }
        if rule_abbr not in rule_map:
            raise ValueError(f"Règle inconnue: {rule_abbr}")

        ordered = rule_map[rule_abbr]()
        return self._respect_precedence(ordered)


def parse_dzn_file(filepath):
    data = {}
    with open(filepath, 'r') as f:
        content = f.read()

    content = re.sub(r'%.*', '', content)  # retirer commentaires

    simple_vars = re.findall(r'(\w+)\s*=\s*([^;]+);', content)
    for var, val in simple_vars:
        val = val.strip()
        if val.isdigit():
            data[var] = int(val)
        elif val.startswith('['):
            val_clean = val.strip('[]')
            data[var] = [int(x) for x in re.findall(r'-?\d+', val_clean)]
        elif val.lower() in ['true', 'false']:
            data[var] = val.lower() == 'true'
        elif val.startswith('{'):
            data[var] = set(int(x) for x in re.findall(r'-?\d+', val))
        else:
            data[var] = val

    for m in ['sreq', 'mastery']:
        pattern = re.compile(rf'{m}\s*=\s*\[\|(.+?)\|\];', re.DOTALL)
        match = pattern.search(content)
        if match:
            matrix_content = match.group(1)
            rows = matrix_content.strip().split('|')
            matrix = []
            for row in rows:
                vals = re.findall(r'\b[\w\d]+\b', row)
                processed_row = []
                for v in vals:
                    if v.lower() == 'true':
                        processed_row.append(True)
                    elif v.lower() == 'false':
                        processed_row.append(False)
                    else:
                        processed_row.append(int(v))
                matrix.append(processed_row)
            data[m] = matrix

    for arr in ['pred', 'succ', 'unpred', 'unsucc']:
        pattern = re.compile(rf'{arr}\s*=\s*\[([^\]]+)\];', re.DOTALL)
        match = pattern.search(content)
        if match:
            val = match.group(1)
            data[arr] = [int(x) for x in re.findall(r'-?\d+', val)]

    precedence_graph = {}
    if 'pred' in data and 'succ' in data:
        for p, s in zip(data['pred'], data['succ']):
            if p not in precedence_graph:
                precedence_graph[p] = {'successors': [], 'predecessors': []}
            if s not in precedence_graph:
                precedence_graph[s] = {'successors': [], 'predecessors': []}
            precedence_graph[p]['successors'].append(s)
            precedence_graph[s]['predecessors'].append(p)
    nActs = data.get('nActs', 0)
    for a in range(1, nActs+1):
        if a not in precedence_graph:
            precedence_graph[a] = {'successors': [], 'predecessors': []}
    data['precedence_graph'] = precedence_graph

    return data


if __name__ == "__main__":
    instances_dir = "./instances"
    dzn_files = glob.glob(f"{instances_dir}/*.dzn")
    if not dzn_files:
        print("Aucune instance .dzn trouvée dans ./instances")
        exit(1)

    for dzn_file in dzn_files:
        print(f"\nChargement de l'instance depuis {dzn_file}")
        instance_data = parse_dzn_file(dzn_file)

        n = instance_data['nActs']
        if 'est' not in instance_data:
            instance_data['est'] = [0]*n
        if 'lst' not in instance_data:
            instance_data['lst'] = [0]*n
        if 'lft' not in instance_data:
            instance_data['lft'] = [0]*n
        if 'float_dyn' not in instance_data:
            instance_data['float_dyn'] = [float('inf')]*n
        if 'resource_usage' not in instance_data:
            instance_data['resource_usage'] = {i+1: 1 for i in range(n)}

        algos = AlgorithmesPriorite(instance_data)

        instance_name = os.path.splitext(os.path.basename(dzn_file))[0]

        for rule in [
            'HRPW*', 'LST', 'LFT',
            'MTS', 'TIMROS', 'HRU1',
            'TIMRES', 'HRU2', 'STFD',
            'EFT'
        ]:
            ordre = algos.get_ordered_activities(rule)

            # Création dossier résultat
            result_dir = f"./resultats/{rule}"
            os.makedirs(result_dir, exist_ok=True)

            # Sauvegarde dans un fichier JSON
            filepath_res = os.path.join(result_dir, f"{instance_name}.json")
            with open(filepath_res, 'w') as f:
                json.dump({
                    "instance": instance_name,
                    "rule": rule,
                    "ordered_activities": ordre,
                    "durations": instance_data["dur"]
                }, f, indent=2)

            print(f"Résultat {rule} sauvegardé dans {filepath_res}")
