import os
import argparse
import re

class O3CPUPowerAnalyzer:
    def __init__(self, stats_path):
        
        # Dictionary of power values (joules per operation or access)
        self.energy_values = {
            # CPU Core Components
        
            'fetch': {
                'icache_tag':9.72e-12,
                'icache_data':2.28e-10,
                'bp_lookups': 6.88e-11,
                'bp_squashes':5.12e-11,
                'btb_lookups': 4.57e-10,
                'btb_updates': 1.73e-9,
                'ras_used': 2.41e-11,
                'ras_pushes':3.54e-11
            },
      
            'decode':{
                'decoded_instructions': 2.83e-10
            },

            'rename':{
                'rename_int_lookups':6.31e-12,
                'rename_fp_lookups':5.18e-12,
                'rename_int_writes':1.32e-11,
                'rename_fp_writes':9.76e-12
            },

            'issueexecutewriteback':{
                'float_mem_read':8.39e-11,
                'float_mem_write':1.31e-10,
                'mem_read':1.12e-10,
                'mem_write':1.84e-10,
                'load_store_forwLoads':2.58e-10,
                'load_store_rescheduledLoads':2.58e-10,
                'load_store_write':2.69e-10,
                'int_alu':8.5e-10,
                'int_mult':8.5e-10,
                'int_div':8.5e-10,
                'float_add':2.55e-9,
                'float_cmp':2.55e-9,
                'float_cvt':2.55e-9,
                'float_mult':2.55e-9,
                'float_mult_acc':2.55e-9,
                'float_div':2.55e-9,
                'float_misc':2.55e-9,
                'float_sqrt':2.55e-9,
                'rob_reads':1.14e-10,
                'rob_writes':1.74e-10,
                'dcache_tag':9.72e-12,
                'dcache_data':2.28e-10
            },
            
            'l2cache':{
                'l2cache_tag':9.4e-11,
                'l2cache_data':1.82e-9

            }
        }
        
        # Logical grouping of components
        self.component_groups = {
            'Fetch': {
                'Icache':[
                    'icache_tag',
                    'icache_data'
                ],
                'Branch Predictor': [
                    'bp_lookups',
                    'bp_squashes'
                ],
                'Branch Target Buffer':[
                    'btb_lookups',
                    'btb_updates'
                ],
                'Return Address Stack':[
                    'ras_used',
                    'ras_pushes'
                ]
            },

            'Decode':{
                'InstructionDecode':[
                    'decoded_instructions'
                ],

            },

            'Rename':{
                'FreeList':[
                'rename_int_lookups',
                'rename_fp_lookups',
                'rename_int_writes',
                'rename_fp_writes'
                ]
            },

            'Issue Execute Writeback':{
                'Register File':[
                    'float_mem_read',
                    'float_mem_write',
                    'mem_read',
                    'mem_write'
                ], 
                'Load Store Queue Read':[
                        'load_store_forwLoads',
                        'load_store_rescheduledLoads'
                    ],
                'Load Store Queue Write':[
                        'load_store_write'
                    ],
                    
                'Integer Operations':[
                    'int_alu',
                    'int_mult',
                    'int_div'
                ],
                'Floating Point Operations':[
                    'float_add',
                    'float_cmp',
                    'float_cvt',
                    'float_mult',
                    'float_mult_acc',
                    'float_div',
                    'float_misc',
                    'float_sqrt'
                ],
                'ROB':[
                    'rob_reads',
                    'rob_writes'
                ],
                'Dcache':[
                    'dcache_tag',
                    'dcache_data'
                ]
  
            },

            'L2Cache':{
                'L2':[
                    'l2cache_tag',
                    'l2cache_data'
                ]

            }

        }
        
        # Regex patterns for stats file parsing
        self.stats_patterns = {

            #Caches
            'icache_tag':r'system\.cpu\.icache\.tags\.tagAccesses\s+(\d+)',
            'icache_data':r'system\.cpu\.icache\.tags\.dataAccesses\s+(\d+)',
            'dcache_tag':r'system\.cpu\.dcache\.tags\.tagAccesses\s+(\d+)',
            'dcache_data':r'system\.cpu\.dcache\.tags\.dataAccesses\s+(\d+)',
            'l2cache_tag':r'system\.l2cache\.tags\.tagAccesses\s+(\d+)',
            'l2cache_data':r'system\.l2cache\.tags\.dataAccesses\s+(\d+)',
     

            #Decoded Instructions
            'decoded_instructions': r'system\.cpu\.decode\.decodedInsts\s+(\d+)',

            # Branch Prediction
            'btb_lookups': r'system\.cpu\.branchPred\.BTBLookups\s+(\d+)',
            'btb_updates': r'system\.cpu\.branchPred\.BTBUpdates\s+(\d+)',
            'bp_lookups': r'system\.cpu\.branchPred\.lookups_0::total\s+(\d+)',
            'bp_squashes': r'system\.cpu\.branchPred\.squashes_0::total\s+(\d+)',
            'ras_used': r'system\.cpu\.branchPred\.ras\.used\s+(\d+)',
            'ras_pushes': r'system\.cpu\.branchPred\.ras\.pushes\s+(\d+)',

            # Register File
            'float_mem_read': r'system\.cpu\.statIssuedInstType_0::FloatMemRead\s+(\d+)',
            'float_mem_write': r'system\.cpu\.statIssuedInstType_0::FloatMemWrite\s+(\d+)',
            'mem_read': r'system\.cpu\.statIssuedInstType_0::MemRead\s+(\d+)',
            'mem_write': r'system\.cpu\.statIssuedInstType_0::MemWrite\s+(\d+)',
            
            # ROB and Rename Stats
            'rob_reads': r'system\.cpu\.rob\.reads\s+(\d+)',
            'rob_writes': r'system\.cpu\.rob\.writes\s+(\d+)',
            'rename_int_lookups': r'system\.cpu\.rename\.intLookups\s+(\d+)',
            'rename_fp_lookups': r'system\.cpu\.rename\.fpLookups\s+(\d+)',
            'rename_int_writes':r'system\.cpu\.rename\.intWrites\s+(\d+)',
            'rename_fp_writes':r'system\.cpu\.rename\.fpWrites\s+(\d+)',

            #Load Store Queue
            'load_store_forwLoads':r'system\.cpu\.lsq0\.forwLoads\s+(\d+)',
            'load_store_rescheduledLoads':r'system\.cpu\.lsq0\.rescheduledLoads\s+(\d+)',
            'load_store_write':r'system\.cpu\.lsq0\.addedLoadsAndStores\s+(\d+)',

    
            # Integer Instructions
            'int_alu': r'system\.cpu\.statIssuedInstType_0::IntAlu\s+(\d+)',
            'int_mult': r'system\.cpu\.statIssuedInstType_0::IntMult\s+(\d+)',
            'int_div': r'system\.cpu\.statIssuedInstType_0::IntDiv\s+(\d+)',

            # Floating Point Instructions
            'float_add': r'system\.cpu\.statIssuedInstType_0::FloatAdd\s+(\d+)',
            'float_cmp': r'system\.cpu\.statIssuedInstType_0::FloatCmp\s+(\d+)',
            'float_cvt': r'system\.cpu\.statIssuedInstType_0::FloatCvt\s+(\d+)',
            'float_mult': r'system\.cpu\.statIssuedInstType_0::FloatMult\s+(\d+)',
            'float_mult_acc': r'system\.cpu\.statIssuedInstType_0::FloatMultAcc\s+(\d+)',
            'float_div': r'system\.cpu\.statIssuedInstType_0::FloatDiv\s+(\d+)',
            'float_misc': r'system\.cpu\.statIssuedInstType_0::FloatMisc\s+(\d+)',
            'float_sqrt': r'system\.cpu\.statIssuedInstType_0::FloatSqrt\s+(\d+)',
    }

 
        
        self.stats_path = stats_path
        self.component_counts = {}
    
    def parse_stats_file(self):
        """
        Automatically search and extract component occurrence counts from the stats file.
        
        """
        # simSeconds
        simulationSeconds = r'simSeconds\s+([\d.]+)'

        try:
            with open(self.stats_path, 'r') as f:
                stats_content = f.read()
                print("Successfully read stats file")
                simSeconds = re.search(simulationSeconds,stats_content)
                global sim_seconds
                sim_seconds = float(simSeconds.group(1))
                print("Sim Seconds",sim_seconds)
            # Extract counts for each component
            for component, pattern in self.stats_patterns.items():
                match = re.search(pattern, stats_content)
                if match:
                    try:
                        value = int(match.group(1))
                        self.component_counts[component] = value
                        print(f"Successfully matched {component}: {value}")
                    except ValueError as ve:
                        print(f"Error converting value for {component}: {ve}")
                else:
                    print(f"No match found for {component} using pattern: {pattern}")
                    self.component_counts[component] = 0

                    # Print final extracted counts
            print("\nFinal Component Counts:")
            for component, count in self.component_counts.items():
                print(f"{component}: {count}")
            print("\n")

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

        global sim_seconds
        # Calculate individual component power
        individual_power = {}
        
        # Iterate through main categories
        for category, components in self.energy_values.items():
            for component, energy_value in components.items():
                if component in self.component_counts:
                    individual_power[component] = (
                        self.component_counts.get(component, 0) * (energy_value/sim_seconds)
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
                f.write("\n## Individual Component Power Consumption (Watts)\n")
                for component, power in individual_power.items():
                    f.write(f"{component}: {power:.6e} W\n")
                
                f.write("\n## Grouped Power Consumption (Watts)\n")
                total_system_power = 0
                
                # Write detailed grouped power with breakdown
                for group, group_data in grouped_power.items():
                    f.write(f"\n{group} Total: {group_data['total']:.6e} W\n")
                    total_system_power += group_data['total']
                    
                    # Write subgroup breakdown
                    for subgroup, subgroup_power in group_data['breakdown'].items():
                        f.write(f"  {subgroup}: {subgroup_power:.6e} W\n")
                
                f.write(f"\nTotal System Power Consumption: {total_system_power:.6e} W\n")
        
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
            print(f"{component}: {power:.6e} W")
        
        print("\nGrouped Power Consumption (Watts):")
        total_system_power = 0
        for group, group_data in grouped_power.items():
            print(f"\n{group} Total: {group_data['total']:.6e} W")
            total_system_power += group_data['total']
            
            # Print subgroup breakdown
            for subgroup, subgroup_power in group_data['breakdown'].items():
                print(f"  {subgroup}: {subgroup_power:.6e} W")
        
        print(f"\nTotal System Power Consumption: {total_system_power:.6e} W")
        
        # Export results to file
        self.export_results(individual_power, grouped_power, output_file)
        print(f"\nPower analysis results exported to {output_file}")

def main():
    # Setup argument parsing
    parser = argparse.ArgumentParser(description='O3CPU Power Model Analyzer')
    parser.add_argument('--stats', default='m5out/stats.txt', 
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
