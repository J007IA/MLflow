#!/usr/bin/env python3
"""
Test script for the Customer Churn Prediction API
Usage: python test_api.py <api_url>
Example: python test_api.py http://localhost:8000
"""

import requests
import json
import sys
from datetime import datetime

def test_health_check(base_url):
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Model loaded: {data['model_loaded']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_model_info(base_url):
    """Test the model info endpoint"""
    print("\n🔍 Testing model info...")
    try:
        response = requests.get(f"{base_url}/model/info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model info retrieved:")
            print(f"   Model type: {data.get('model_type', 'N/A')}")
            print(f"   Feature count: {data.get('feature_count', 'N/A')}")
            return True
        else:
            print(f"❌ Model info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model info error: {e}")
        return False

def test_single_prediction(base_url):
    """Test single customer prediction"""
    print("\n🔍 Testing single prediction...")
    
    # Sample customer data
    customer_data = {
        "EDAD": 35,
        "GENERO": "M",
        "ESTADO_CIVIL": "Casado",
        "RENTA": 75000,
        "SEGMENTO": "B",
        "TOTAL_REQUERIMIENTOS": 5,
        "TOTAL_RECLAMOS": 2,
        "PORC_RECLAMOS": 0.4,
        "TOTAL_PROCDE": 1,
        "PORC_PROCDE": 0.2,
        "MESES_ACTIVOS": 6,
        "REQ_PROM_MES": 0.83
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict?customer_id=test_001",
            json=customer_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful:")
            print(f"   Customer ID: {data['customer_id']}")
            print(f"   Churn probability: {data['churn_probability']:.4f}")
            print(f"   Churn prediction: {data['churn_prediction']}")
            print(f"   Risk level: {data['risk_level']}")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def test_batch_prediction(base_url):
    """Test batch prediction"""
    print("\n🔍 Testing batch prediction...")
    
    # Sample batch data
    customers = [
        {
            "EDAD": 28,
            "GENERO": "F",
            "RENTA": 45000,
            "SEGMENTO": "C",
            "TOTAL_REQUERIMIENTOS": 2,
            "TOTAL_RECLAMOS": 0,
            "PORC_RECLAMOS": 0.0
        },
        {
            "EDAD": 45,
            "GENERO": "M",
            "RENTA": 95000,
            "SEGMENTO": "A",
            "TOTAL_REQUERIMIENTOS": 8,
            "TOTAL_RECLAMOS": 5,
            "PORC_RECLAMOS": 0.625
        }
    ]
    
    try:
        response = requests.post(
            f"{base_url}/predict/batch",
            json=customers,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Batch prediction successful:")
            print(f"   Processed customers: {data['count']}")
            for i, pred in enumerate(data['predictions']):
                print(f"   Customer {i+1}: {pred['churn_probability']:.4f} ({pred['risk_level']})")
            return True
        else:
            print(f"❌ Batch prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Batch prediction error: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_api.py <api_url>")
        print("Example: python test_api.py http://localhost:8000")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print(f"🚀 Testing Customer Churn Prediction API at: {base_url}")
    print(f"📅 Test started at: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Health Check", test_health_check),
        ("Model Info", test_model_info),
        ("Single Prediction", test_single_prediction),
        ("Batch Prediction", test_batch_prediction)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func(base_url)
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
    
    print(f"\n🏆 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Check the API deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main() 