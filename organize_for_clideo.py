#!/usr/bin/env python3
"""
Organize Audio Files for Clideo
Copies and renames files in correct order for easy merging
"""

import os
import shutil
from pathlib import Path

def organize_demo_files():
    """Organize all demo files for easy merging"""
    
    print("\n" + "="*60)
    print("Audio File Organizer for Clideo")
    print("="*60 + "\n")
    
    # Create output directory
    demos_ready = Path("recordings/demos_ready_to_merge")
    demos_ready.mkdir(exist_ok=True)
    
    # Demo 1: Appointment Scheduling
    print("📁 Organizing DEMO 1: Appointment Scheduling...")
    demo1_dir = demos_ready / "demo1_appointment"
    demo1_dir.mkdir(exist_ok=True)
    
    appointment_files = [
        ("appointment_01_greeting.mp3", "01_assistant_greeting.mp3"),
        ("user_voice/appointment_user_01.mp3", "02_user.mp3"),
        ("appointment_02_response.mp3", "03_assistant.mp3"),
        ("user_voice/appointment_user_02.mp3", "04_user.mp3"),
        ("appointment_03_response.mp3", "05_assistant.mp3"),
        ("user_voice/appointment_user_03.mp3", "06_user.mp3"),
        ("appointment_04_response.mp3", "07_assistant.mp3"),
        ("user_voice/appointment_user_04.mp3", "08_user.mp3"),
        ("appointment_05_response.mp3", "09_assistant.mp3"),
        ("user_voice/appointment_user_05.mp3", "10_user.mp3"),
        ("appointment_06_response.mp3", "11_assistant.mp3"),
        ("user_voice/appointment_user_06.mp3", "12_user.mp3"),
        ("appointment_07_response.mp3", "13_assistant.mp3"),
        ("user_voice/appointment_user_07.mp3", "14_user.mp3"),
        ("appointment_08_response.mp3", "15_assistant.mp3"),
        ("user_voice/appointment_user_08.mp3", "16_user.mp3"),
        ("appointment_09_response.mp3", "17_assistant.mp3"),
        ("user_voice/appointment_user_09.mp3", "18_user.mp3"),
        ("appointment_10_response.mp3", "19_assistant.mp3"),
        ("user_voice/appointment_user_10.mp3", "20_user.mp3"),
        ("appointment_final_closing.mp3", "21_closing.mp3"),
    ]
    
    copy_files(appointment_files, demo1_dir)
    print(f"✓ {len(appointment_files)} files organized in: {demo1_dir}\n")
    
    # Demo 2: Insurance Verification
    print("📁 Organizing DEMO 2: Insurance Verification...")
    demo2_dir = demos_ready / "demo2_insurance"
    demo2_dir.mkdir(exist_ok=True)
    
    insurance_files = [
        ("insurance_01_greeting.mp3", "01_assistant_greeting.mp3"),
        ("user_voice/insurance_user_01.mp3", "02_user.mp3"),
        ("insurance_02_response.mp3", "03_assistant.mp3"),
        ("user_voice/insurance_user_02.mp3", "04_user.mp3"),
        ("insurance_03_response.mp3", "05_assistant.mp3"),
        ("user_voice/insurance_user_03.mp3", "06_user.mp3"),
        ("insurance_04_response.mp3", "07_assistant.mp3"),
        ("user_voice/insurance_user_04.mp3", "08_user.mp3"),
        ("insurance_05_response.mp3", "09_assistant.mp3"),
        ("user_voice/insurance_user_05.mp3", "10_user.mp3"),
        ("insurance_final_closing.mp3", "11_closing.mp3"),
    ]
    
    copy_files(insurance_files, demo2_dir)
    print(f"✓ {len(insurance_files)} files organized in: {demo2_dir}\n")
    
    # Demo 3: Edge Case
    print("📁 Organizing DEMO 3: Edge Case (No Available Slot)...")
    demo3_dir = demos_ready / "demo3_edge_case"
    demo3_dir.mkdir(exist_ok=True)
    
    edge_case_files = [
        ("appointment_no_slot_01_greeting.mp3", "01_assistant_greeting.mp3"),
        ("user_voice/edge_case_user_01.mp3", "02_user.mp3"),
        ("appointment_no_slot_02_response.mp3", "03_assistant.mp3"),
        ("user_voice/edge_case_user_02.mp3", "04_user.mp3"),
        ("appointment_no_slot_03_response.mp3", "05_assistant.mp3"),
        ("user_voice/edge_case_user_03.mp3", "06_user.mp3"),
        ("appointment_no_slot_04_response.mp3", "07_assistant.mp3"),
        ("user_voice/edge_case_user_04.mp3", "08_user.mp3"),
        ("appointment_no_slot_05_response.mp3", "09_assistant.mp3"),
        ("user_voice/edge_case_user_05.mp3", "10_user.mp3"),
        ("appointment_no_slot_06_response.mp3", "11_assistant.mp3"),
        ("user_voice/edge_case_user_06.mp3", "12_user.mp3"),
        ("appointment_no_slot_07_response.mp3", "13_assistant.mp3"),
        ("user_voice/edge_case_user_07.mp3", "14_user.mp3"),
        ("appointment_no_slot_08_response.mp3", "15_assistant.mp3"),
        ("user_voice/edge_case_user_08.mp3", "16_user.mp3"),
        ("appointment_no_slot_09_response.mp3", "17_assistant.mp3"),
        ("user_voice/edge_case_user_09.mp3", "18_user.mp3"),
        ("appointment_no_slot_final_closing.mp3", "19_closing.mp3"),
    ]
    
    copy_files(edge_case_files, demo3_dir)
    print(f"✓ {len(edge_case_files)} files organized in: {demo3_dir}\n")
    
    # Final instructions
    print("="*60)
    print("✅ All files organized and ready!")
    print("="*60)
    print("\nNEXT STEPS:")
    print("\n1. Go to: https://clideo.com/merge-audio")
    print("\n2. For DEMO 1 (Appointment):")
    print(f"   - Open folder: {demo1_dir}")
    print("   - Select ALL files (Ctrl+A)")
    print("   - Drag them to Clideo")
    print("   - Export as: DEMO_1_Appointment_Full.mp3")
    print("\n3. For DEMO 2 (Insurance):")
    print(f"   - Open folder: {demo2_dir}")
    print("   - Select ALL files (Ctrl+A)")
    print("   - Drag them to Clideo")
    print("   - Export as: DEMO_2_Insurance_Full.mp3")
    print("\n4. For DEMO 3 (Edge Case):")
    print(f"   - Open folder: {demo3_dir}")
    print("   - Select ALL files (Ctrl+A)")
    print("   - Drag them to Clideo")
    print("   - Export as: DEMO_3_EdgeCase_Full.mp3")
    print("\n" + "="*60 + "\n")
    print("💡 TIP: Files are numbered in order, so if you select all")
    print("        and drag to Clideo, they'll be in perfect order!")
    print("\n" + "="*60 + "\n")


def copy_files(file_list, dest_dir):
    """Copy files with new names to destination directory"""
    recordings_dir = Path("recordings")
    
    for source_rel, dest_name in file_list:
        source = recordings_dir / source_rel
        dest = dest_dir / dest_name
        
        if source.exists():
            shutil.copy2(source, dest)
            print(f"  ✓ {source_rel} → {dest_name}")
        else:
            print(f"  ⚠ Warning: {source_rel} not found")


if __name__ == "__main__":
    try:
        organize_demo_files()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
