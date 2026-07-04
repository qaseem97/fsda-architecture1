import numpy as np
from fsda_client import FSDA

def run_fsda_with_output():
    fs = FSDA()
    
    # 1. Input Data
    cont_table = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]
    random_data = np.random.rand(10, 3).tolist()
    
    print("--- Starting FSDA Analysis ---\n")
    
    # Execution and Output Printing
    try:
        # zscoreFS
        z_res = fs.zscoreFS(random_data)
        print(f"1. zscoreFS Output (Sample): {z_res[0][:3]}")

        # getYahoo
        yahoo = fs.getYahoo('AAPL', 'plots', False, 'LastPeriod', '1mo')
        print(f"2. getYahoo Output: Ticker={yahoo.get('Ticker')}, Success={yahoo.get('Success')}")

        # CorAna
        cor_res = fs.CorAna(cont_table)
        print(f"3. CorAna Output: {cor_res}")

        # FSM
        fsm_res = fs.FSM(random_data)
        print(f"4. FSM Output: {fsm_res}")

        # FSD
        fsd_res = fs.FSD(random_data)
        print(f"5. FSD Output: {fsd_res}")
        
        print("\n--- All operations completed successfully! ---")

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    run_fsda_with_output()