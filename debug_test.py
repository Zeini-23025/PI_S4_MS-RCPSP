#!/usr/bin/env python3
"""
Debug script to identify the exact source of the 'list' object has no attribute 'get' error
"""

import sys
import os
import glob
import json
import traceback

# Import the necessary modules
from paste import parse_dzn_file, compute_temporal_metrics, MSRCPSPPriorityAlgorithms


def test_algorithm_generation():
    """Test the algorithm generation phase"""
    print("="*60)
    print("TESTING ALGORITHM GENERATION")
    print("="*60)
    
    instances_dir = "./instances"
    dzn_files = glob.glob(os.path.join(instances_dir, "*.dzn"))[:5]  # Test first 5 files
    
    print(f"Testing {len(dzn_files)} instance(s)...")
    
    for dzn_file in dzn_files:
        instance_name = os.path.splitext(os.path.basename(dzn_file))[0]
        print(f"Processing: {instance_name}")
        
        try:
            # Load and process instance
            instance_data = parse_dzn_file(dzn_file)
            instance_data = compute_temporal_metrics(instance_data)
            
            # Create algorithms object
            algorithms_obj = MSRCPSPPriorityAlgorithms(instance_data)
            
            # Get all priority orders
            all_orders = algorithms_obj.get_all_priority_orders()
            
            # Save results
            for rule_name, activity_order in all_orders.items():
                rule_dir = os.path.join("./resultats", rule_name)
                os.makedirs(rule_dir, exist_ok=True)
                
                output_data = {
                    "instance": instance_name,
                    "rule": rule_name,
                    "n_activities": instance_data.get('nActs', 0),
                    "ordered_activities": activity_order,
                    "durations": instance_data.get('dur', [])
                }
                
                output_file = os.path.join(rule_dir, f"{instance_name}.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✓ Success: Generated results for {len(all_orders)} algorithms")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            traceback.print_exc()
            return False
    
    return True


def test_makespan_calculation():
    """Test the makespan calculation phase"""
    print("\n" + "="*60)
    print("TESTING MAKESPAN CALCULATION")
    print("="*60)
    
    try:
        from makespan_calculator import MakespanCalculator
        
        calculator = MakespanCalculator()
        
        # Test loading a single instance
        instance_name = "inst_set1a_sf0_nc1.5_n20_m10_00"  # Use a simple instance
        
        print(f"Testing instance data loading for: {instance_name}")
        try:
            instance_data = calculator.load_instance_data(instance_name)
            print(f"  ✓ Instance data loaded successfully")
            print(f"  Data keys: {list(instance_data.keys())}")
            print(f"  Instance data type: {type(instance_data)}")
        except Exception as e:
            print(f"  ✗ Error loading instance data: {e}")
            traceback.print_exc()
            return False
        
        # Test loading algorithm results
        algorithms = ['HRPW*', 'LST', 'LFT']
        for algorithm in algorithms:
            print(f"Testing algorithm result loading for: {algorithm}")
            try:
                result = calculator.load_algorithm_result(algorithm, instance_name)
                print(f"  ✓ {algorithm} result loaded: {type(result)} with {len(result)} activities")
            except FileNotFoundError:
                print(f"  ! {algorithm} result file not found (expected if not generated yet)")
            except Exception as e:
                print(f"  ✗ Error loading {algorithm} result: {e}")
                print(f"  Error type: {type(e)}")
                traceback.print_exc()
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error importing MakespanCalculator: {e}")
        traceback.print_exc()
        return False


def main():
    """Main debug function"""
    print("DEBUG SCRIPT FOR MS-RCPSP ERROR DIAGNOSIS")
    print("="*60)
    
    # Check if results directory exists
    if not os.path.exists("./resultats"):
        os.makedirs("./resultats", exist_ok=True)
        print("Created results directory")
    
    # Test algorithm generation first
    if not test_algorithm_generation():
        print("Algorithm generation failed. Stopping.")
        return
    
    # Test makespan calculation
    if not test_makespan_calculation():
        print("Makespan calculation failed.")
        return
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED SUCCESSFULLY")
    print("="*60)


if __name__ == "__main__":
    main()
