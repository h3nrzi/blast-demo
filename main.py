import sys
import subprocess
import time

def run_step(step_name: str, script_path: str):
    print(f"\n==========================================")
    print(f"▶ LAYER 2 ORCHESTRATOR: Running {step_name}")
    print(f"  Script: {script_path}")
    print(f"==========================================")
    start_time = time.time()
    
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    duration = time.time() - start_time
    
    if result.returncode == 0:
        print(f"✅ {step_name} COMPLETED ({duration:.2f}s)")
        print(result.stdout.strip())
    else:
        print(f"❌ {step_name} FAILED ({duration:.2f}s)")
        print("STDOUT:", result.stdout.strip())
        print("STDERR:", result.stderr.strip())
        sys.exit(result.returncode)

def main():
    print("🚀 Starting B.L.A.S.T. Layer 2 Pipeline Orchestrator")
    
    # Step 1: Raw Ingestion Tool (Layer 3)
    run_step("1. Raw RSS Ingestion", "tools/fetch_rss_raw.py")
    
    # Step 2: Categorization & Formatting Tool (Layer 3)
    run_step("2. Taxonomy Classification & Payload Formatting", "tools/categorize_articles.py")
    
    print("\n🎉 Pipeline Execution Completed Successfully!")

if __name__ == "__main__":
    main()
