#!/usr/bin/env python3
"""Test script to verify the new import structure works"""

from st_img_picker import img_picker

def test_basic_functionality():
    """Test basic functionality without actually running Streamlit"""
    
    # Test 1: Check function exists and is callable
    print("✅ img_picker function imported successfully")
    assert callable(img_picker), "img_picker should be callable"
    
    # Test 2: Check default parameters
    import inspect
    sig = inspect.signature(img_picker)
    assert sig.parameters['allow_multiple'].default == True, "allow_multiple should default to True"
    print("✅ allow_multiple defaults to True")
    
    # Test 3: Verify function name
    assert img_picker.__name__ == 'img_picker', f"Function name should be img_picker, got {img_picker.__name__}"
    print("✅ Function name is correct")
    
    print("\n🎉 All tests passed! The import structure is working correctly.")
    
    print("\nYou can now use:")
    print("from st_img_picker import img_picker")
    print("imgs = img_picker('Label', ['img1.png', 'img2.png'])  # Multi-select by default")

if __name__ == "__main__":
    test_basic_functionality()