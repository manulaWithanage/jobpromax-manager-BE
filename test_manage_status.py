"""
Test script for Manage Status API endpoints.
Tests: IncidentReports, ActivityLog, and enhanced Features with history.
"""
import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"


async def test_manage_status_api():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        
        # ========================================
        # TEST 1: Login as Manager
        # ========================================
        print("=" * 60)
        print("TEST 1: Login as Manager")
        print("=" * 60)
        
        login_resp = await client.post("/auth/login", json={
            "email": "manager@jobpromax.com",
            "password": "manager123"
        })
        print(f"Status: {login_resp.status_code}")
        print(f"Response: {login_resp.json()}")
        
        cookies = login_resp.cookies
        if login_resp.status_code != 200:
            print("ERROR: Login failed, cannot continue tests")
            return
        
        # ========================================
        # TEST 2: Create Incident Report
        # ========================================
        print("\n" + "=" * 60)
        print("TEST 2: Create Incident Report (as authenticated user)")
        print("=" * 60)
        
        report_resp = await client.post("/api/reports/", json={
            "reporterName": "Test Reporter",
            "reporterEmail": "test@example.com",
            "impactLevel": "high",
            "description": "Test issue: API returning 500 errors on payment endpoint"
        }, cookies=cookies)
        print(f"Status: {report_resp.status_code}")
        print(f"Response: {report_resp.json()}")
        
        report_id = None
        if report_resp.status_code == 200:
            report_id = report_resp.json().get("id")
            print(f"Created report ID: {report_id}")
        
        # ========================================
        # TEST 3: List Reports
        # ========================================
        print("\n" + "=" * 60)
        print("TEST 3: List Reports (Manager only)")
        print("=" * 60)
        
        list_resp = await client.get("/api/reports/", cookies=cookies)
        print(f"Status: {list_resp.status_code}")
        reports = list_resp.json()
        print(f"Total reports: {len(reports)}")
        for r in reports[:3]:  # Show first 3
            print(f"  - {r['id']}: {r['description'][:40]}... ({r['status']})")
        
        # ========================================
        # TEST 4: Update Report Status
        # ========================================
        if report_id:
            print("\n" + "=" * 60)
            print("TEST 4: Update Report Status to 'acknowledged'")
            print("=" * 60)
            
            status_resp = await client.patch(f"/api/reports/{report_id}/status", json={
                "status": "acknowledged"
            }, cookies=cookies)
            print(f"Status: {status_resp.status_code}")
            print(f"Response: {status_resp.json()}")
        
        # ========================================
        # TEST 5: Add Note to Report
        # ========================================
        if report_id:
            print("\n" + "=" * 60)
            print("TEST 5: Add Admin Note to Report")
            print("=" * 60)
            
            note_resp = await client.post(f"/api/reports/{report_id}/notes", json={
                "note": "Investigating this issue. Appears related to recent deployment."
            }, cookies=cookies)
            print(f"Status: {note_resp.status_code}")
            if note_resp.status_code == 200:
                report = note_resp.json()
                print(f"Notes count: {len(report.get('adminNotes', []))}")
        
        # ========================================
        # TEST 6: Get Features (with new fields)
        # ========================================
        print("\n" + "=" * 60)
        print("TEST 6: Get Features (check for history/lastUpdatedBy)")
        print("=" * 60)
        
        features_resp = await client.get("/features", cookies=cookies)
        print(f"Status: {features_resp.status_code}")
        features = features_resp.json()
        print(f"Total features: {len(features)}")
        
        feature_id = None
        if features:
            feature = features[0]
            feature_id = feature.get("id") or feature.get("_id")
            print(f"First feature: {feature.get('name')} - {feature.get('status')}")
            print(f"  History entries: {len(feature.get('history', []))}")
            print(f"  Last updated by: {feature.get('lastUpdatedBy')}")
        
        # ========================================
        # TEST 7: Update Feature Status (triggers history)
        # ========================================
        if feature_id:
            print("\n" + "=" * 60)
            print("TEST 7: Update Feature Status (triggers history tracking)")
            print("=" * 60)
            
            update_resp = await client.patch(f"/features/{feature_id}", json={
                "status": "degraded"
            }, cookies=cookies)
            print(f"Status: {update_resp.status_code}")
            if update_resp.status_code == 200:
                updated = update_resp.json()
                print(f"Updated feature: {updated.get('name')} → {updated.get('status')}")
                print(f"  History entries: {len(updated.get('history', []))}")
                print(f"  Last updated by: {updated.get('lastUpdatedBy')}")
        
        # ========================================
        # TEST 8: Get Activities
        # ========================================
        print("\n" + "=" * 60)
        print("TEST 8: Get All Activities (Manager only)")
        print("=" * 60)
        
        activities_resp = await client.get("/api/activities/", cookies=cookies)
        print(f"Status: {activities_resp.status_code}")
        activities = activities_resp.json()
        print(f"Total activities: {len(activities)}")
        for a in activities[:5]:  # Show first 5
            print(f"  - {a['action']}: {a['userName']} @ {a['timestamp']}")
        
        # ========================================
        # TEST 9: Get My Activities
        # ========================================
        print("\n" + "=" * 60)
        print("TEST 9: Get My Activities (authenticated user)")
        print("=" * 60)
        
        my_activities_resp = await client.get("/api/activities/me", cookies=cookies)
        print(f"Status: {my_activities_resp.status_code}")
        my_activities = my_activities_resp.json()
        print(f"My activities: {len(my_activities)}")
        
        # ========================================
        # TEST 10: Delete Report (cleanup)
        # ========================================
        if report_id:
            print("\n" + "=" * 60)
            print("TEST 10: Delete Report (cleanup)")
            print("=" * 60)
            
            del_resp = await client.delete(f"/api/reports/{report_id}", cookies=cookies)
            print(f"Status: {del_resp.status_code}")
            print(f"Response: {del_resp.json()}")
        
        # ========================================
        # TEST 11: Logout
        # ========================================
        print("\n" + "=" * 60)
        print("TEST 11: Logout (verify LOGOUT activity logged)")
        print("=" * 60)
        
        logout_resp = await client.post("/auth/logout", cookies=cookies)
        print(f"Status: {logout_resp.status_code}")
        print(f"Response: {logout_resp.json()}")
        
        # ========================================
        # SUMMARY
        # ========================================
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_manage_status_api())
