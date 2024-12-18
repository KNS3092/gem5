import os
import argparse
import re

class O3CPUPowerAnalyzer:
    def __init__(self, stats_path):
        """
        Initialize the power analyzer with configurable power values and component mappings.

        """
        # Dictionary of power values (watts per operation or access)
        self.power_values = {
            # CPU Core Components
            'integer_operations': {
                'integer_alu': 0.5,
                'integer_multiply': 0.7,
                'integer_divide': 1.2
            },
            'floating_point_operations': {
                'fp_alu': 0.8,
                'fp_multiply': 1.0,
                'fp_divide': 1.5
            },
            'branch_prediction': {
                'branch_predictor': 0.3,
                'btb': 0.2,
                'ras': 0.15
            },
            'instruction_processing': {
                'instruction_fetch': 0.4,
                'instruction_decode': 0.3,
                'instruction_issue': 0.35
            },
            'memory_access': {
                'l1_dcache_read': 0.2,
                'l1_dcache_write': 0.25,
                'l1_icache_read': 0.15,
                'l2_cache_read': 0.4,
                'l2_cache_write': 0.45
            },
            'register_file': {
                'integer_register_file': 0.1,
                'fp_register_file': 0.15,
                'register_read': 0.05,
                'register_write': 0.06
            }
        }
        
        # Logical grouping of components
        self.component_groups = {
            'Compute': {
                'Integer Operations': [
                    'integer_alu', 
                    'integer_multiply', 
                    'integer_divide'
                ],
                'Floating Point Operations': [
                    'fp_alu', 
                    'fp_multiply', 
                    'fp_divide'
                ]
            },
            'Control Flow': {
                'Branch Prediction': [
                    'branch_predictor', 
                    'btb', 
                    'ras'
                ],
                'Instruction Processing': [
                    'instruction_fetch', 
                    'instruction_decode', 
                    'instruction_issue'
                ]
            },
            'Memory': {
                'Cache Reads': [
                    'l1_dcache_read', 
                    'l1_icache_read', 
                    'l2_cache_read'
                ],
                'Cache Writes': [
                    'l1_dcache_write', 
                    'l2_cache_write'
                ]
            },
            'Register Management': {
                'Register Operations': [
                    'integer_register_file', 
                    'fp_register_file', 
                    'register_read', 
                    'register_write'
                ]
            }
        }
        
        # Regex patterns for stats file parsing
        self.stats_patterns = {
            'integer_alu': r'system\.cpu\.exec_context\.number_of_integer_alu_accesses\s*(\d+)',
            'integer_multiply': r'system\.cpu\.exec_context\.number_of_integer_multiply_accesses\s*(\d+)',
            'integer_divide': r'system\.cpu\.exec_context\.number_of_integer_divide_accesses\s*(\d+)',
            'fp_alu': r'system\.cpu\.exec_context\.number_of_fp_alu_accesses\s*(\d+)',
            'fp_multiply': r'system\.cpu\.exec_context\.number_of_fp_multiply_accesses\s*(\d+)',
            'fp_divide': r'system\.cpu\.exec_context\.number_of_fp_divide_accesses\s*(\d+)',
            'branch_predictor': r'system\.cpu\.branchPred\.num_predictions\s*(\d+)',
            'btb': r'system\.cpu\.branchPred\.btb\.hits\s*(\d+)',
            'ras': r'system\.cpu\.branchPred\.ras\.used\s*(\d+)',
            'instruction_fetch': r'system\.cpu\.icache\.overall_hits::total\s*(\d+)',
            'instruction_decode': r'system\.cpu\.instruction_decoder\.total_instructions\s*(\d+)',
            'instruction_issue': r'system\.cpu\.instruction_issue\.total_instructions\s*(\d+)',
            'l1_dcache_read': r'system\.cpu\.dcache\.overall_hits::Read\s*(\d+)',
            'l1_dcache_write': r'system\.cpu\.dcache\.overall_hits::Write\s*(\d+)',
            'l1_icache_read': r'system\.cpu\.icache\.overall_hits::Read\s*(\d+)',
            'l2_cache_read': r'system\.l2\.overall_hits::Read\s*(\d+)',
            'l2_cache_write': r'system\.l2\.overall_hits::Write\s*(\d+)',
            'integer_register_file': r'system\.cpu\.int_regfile_reads\s*(\d+)',
            'fp_register_file': r'system\.cpu\.fp_regfile_reads\s*(\d+)',
            'register_read': r'system\.cpu\.total_register_reads\s*(\d+)',
            'register_write': r'system\.cpu\.total_register_writes\s*(\d+)'
        }
        
        self.stats_path = stats_path
        self.component_counts = {}
    
    def parse_stats_file(self):
        """
        Automatically search and extract component occurrence counts from the stats file.
        
        """
        try:
            with open(self.stats_path, 'r') as f:
                stats_content = f.read()
            
            # Extract counts for each component
            for component, pattern in self.stats_patterns.items():
                match = re.search(pattern, stats_content)
                if match:
                    self.component_counts[component] = int(match.group(1))
                else:
                    self.component_counts[component] = 0
        
        except FileNotFoundError:
            print(f"Error: Stats file not found at {self.stats_path}")
            raise
        except Exception as e:
            print(f"Error parsing stats file: {e}")
            raise
    
    def calculate_power(self):
        """
        Calculate power consumption for each component and group
        
        Returns:
        - Individual component power consumptions
        - Grouped power consumptions
        - Sub-Group power consumptions
        - Total power comsumptions
        """
        # Calculate individual component power
        individual_power = {}
        
        # Iterate through main categories
        for category, components in self.power_values.items():
            for component, power_value in components.items():
                if component in self.component_counts:
                    individual_power[component] = (
                        self.component_counts.get(component, 0) * power_value
                    )
        
        # Calculate grouped power
        grouped_power = {}
        
        # Iterate through main groups
        for group, subgroups in self.component_groups.items():
            group_total = 0
            group_breakdown = {}
            
            # Iterate through subgroups
            for subgroup, components in subgroups.items():
                subgroup_total = sum(
                    individual_power.get(comp, 0) for comp in components
                )
                group_total += subgroup_total
                group_breakdown[subgroup] = subgroup_total
            
            grouped_power[group] = {
                'total': group_total,
                'breakdown': group_breakdown
            }
        
        return individual_power, grouped_power
    
    def export_results(self, individual_power, grouped_power, output_file):
        """
        Export power analysis results to a text file with detailed nested structure.
        """
        try:
            with open(output_file, 'w') as f:
                f.write("# O3CPU Power Analysis Results\n\n")
                
                # Write individual component power
                f.write("## Individual Component Power Consumption (Watts)\n")
                for component, power in individual_power.items():
                    f.write(f"{component}: {power:.4f} W\n")
                
                f.write("\n## Grouped Power Consumption (Watts)\n")
                total_system_power = 0
                
                # Write detailed grouped power with breakdown
                for group, group_data in grouped_power.items():
                    f.write(f"\n{group} Total: {group_data['total']:.4f} W\n")
                    total_system_power += group_data['total']
                    
                    # Write subgroup breakdown
                    for subgroup, subgroup_power in group_data['breakdown'].items():
                        f.write(f"  {subgroup}: {subgroup_power:.4f} W\n")
                
                f.write(f"\nTotal System Power Consumption: {total_system_power:.4f} W\n")
        
        except Exception as e:
            print(f"Error exporting results: {e}")
    
    def run_analysis(self, output_file):
        """
        Run complete power analysis workflow.
        """
        # Parse stats file to get component counts
        self.parse_stats_file()
        
        # Calculate power consumption
        individual_power, grouped_power = self.calculate_power()
        
        # Display results
        print("Individual Component Power Consumption (Watts):")
        for component, power in individual_power.items():
            print(f"{component}: {power:.4f} W")
        
        print("\nGrouped Power Consumption (Watts):")
        total_system_power = 0
        for group, group_data in grouped_power.items():
            print(f"\n{group} Total: {group_data['total']:.4f} W")
            total_system_power += group_data['total']
            
            # Print subgroup breakdown
            for subgroup, subgroup_power in group_data['breakdown'].items():
                print(f"  {subgroup}: {subgroup_power:.4f} W")
        
        print(f"\nTotal System Power Consumption: {total_system_power:.4f} W")
        
        # Export results to file
        self.export_results(individual_power, grouped_power, output_file)
        print(f"\nPower analysis results exported to {output_file}")

def main():
    # Setup argument parsing
    parser = argparse.ArgumentParser(description='O3CPU Power Model Analyzer')
    parser.add_argument('--stats', default='m5out/stats_test.txt', 
                        help='Path to the gem5 stats file (default: m5out/stats.txt)')
    parser.add_argument('--output', default='O3CPU_Power_Model/O3CPU_power_analysis_results.txt', 
                        help='Output file for power analysis results')
    
    # Parse arguments
    args = parser.parse_args()
    
    
    # Perform power analysis
    analyzer = O3CPUPowerAnalyzer(args.stats)
    analyzer.run_analysis(args.output)

if __name__ == '__main__':
    main()