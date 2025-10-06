# Django ORM Practice Session
# Based on your Sigma Sync Technologies Models
# Work through these questions one by one

from django.db import models
from django.db.models import Q, Count, Sum, Avg, Max, Min, F, Case, When
from django.utils import timezone
from datetime import datetime, timedelta

# Import your models (uncomment when ready to test)
# from your_app.models import (
#     LoanConfigurationsProcessModel, 
#     RegionConfigurationRegionModel,
#     UserModel, 
#     AllocationFileModel,
#     CaseManagementCaseModel,
#     # ... other models
# )

"""
🎯 PRACTICE SESSION 1: BEGINNER LEVEL (10 Questions)
Work through these step by step. Write your answers below each question.
"""

print("="*60)
print("🚀 DJANGO ORM PRACTICE SESSION")
print("="*60)

# QUESTION 1: Basic Filtering
print("\n📝 QUESTION 1:")
print("Get all active users from UserModel")
print("Hint: Filter by is_active=True")

# Write your answer here:
# active_users = 


# QUESTION 2: Count Records
print("\n📝 QUESTION 2:")
print("Count total number of loan processes")
print("Hint: Use .count() method")

# Write your answer here:
# process_count = 


# QUESTION 3: Field Lookups
print("\n📝 QUESTION 3:")
print("Find all users whose email contains 'gmail.com'")
print("Hint: Use __icontains lookup")

# Write your answer here:
# gmail_users = 


# QUESTION 4: Exclude Query
print("\n📝 QUESTION 4:")
print("Get all users except superusers")
print("Hint: Use .exclude() method")

# Write your answer here:
# non_superusers = 


# QUESTION 5: Ordering
print("\n📝 QUESTION 5:")
print("Get all regions ordered by title alphabetically")
print("Hint: Use .order_by('title')")

# Write your answer here:
# ordered_regions = 


# QUESTION 6: Date Filtering
print("\n📝 QUESTION 6:")
print("Find users created in the last 30 days")
print("Hint: Use timezone.now() - timedelta(days=30)")

# Write your answer here:
# recent_users = 


# QUESTION 7: Null Checks
print("\n📝 QUESTION 7:")
print("Find all processes where contact_person_email is NOT null")
print("Hint: Use __isnull=False")

# Write your answer here:
# processes_with_email = 


# QUESTION 8: Multiple Conditions
print("\n📝 QUESTION 8:")
print("Find users who are both active AND verified")
print("Hint: Chain multiple filter conditions")

# Write your answer here:
# active_verified_users = 


# QUESTION 9: First/Last Record
print("\n📝 QUESTION 9:")
print("Get the most recently created allocation file")
print("Hint: Use .order_by('-created_date').first()")

# Write your answer here:
# latest_allocation = 


# QUESTION 10: Field Selection
print("\n📝 QUESTION 10:")
print("Get only usernames and emails of all users")
print("Hint: Use .values('username', 'email')")

# Write your answer here:
# user_data = 


print("\n" + "="*60)
print("🎯 PRACTICE SESSION 2: INTERMEDIATE LEVEL (10 Questions)")
print("="*60)

# QUESTION 11: Foreign Key Relationships
print("\n📝 QUESTION 11:")
print("Get all zones with their region titles")
print("Hint: Use select_related() for foreign keys")

# Write your answer here:
# zones_with_regions = 


# QUESTION 12: Reverse Foreign Key
print("\n📝 QUESTION 12:")
print("Get a specific region with all its zones")
print("Hint: Use _set manager or related_name")

# Write your answer here:
# region_with_zones = 


# QUESTION 13: Aggregation
print("\n📝 QUESTION 13:")
print("Count number of cases per bucket")
print("Hint: Use .values('bucket').annotate(count=Count('id'))")

# Write your answer here:
# cases_per_bucket = 


# QUESTION 14: Q Objects
print("\n📝 QUESTION 14:")
print("Find users who are either staff OR superuser")
print("Hint: Use Q(is_staff=True) | Q(is_superuser=True)")

# Write your answer here:
# staff_or_super = 


# QUESTION 15: Date Range
print("\n📝 QUESTION 15:")
print("Find allocation files created between two specific dates")
print("Hint: Use __range lookup")

# Write your answer here:
# files_in_range = 


# QUESTION 16: Many-to-Many
print("\n📝 QUESTION 16:")
print("Get all users assigned to a specific region")
print("Hint: Use assigned_region field")

# Write your answer here:
# region_users = 


# QUESTION 17: Complex Filtering
print("\n📝 QUESTION 17:")
print("Find cases where total_loan_amount > 100000 AND current_dpd > 30")
print("Hint: Chain multiple conditions")

# Write your answer here:
# high_value_overdue = 


# QUESTION 18: Aggregation with Grouping
print("\n📝 QUESTION 18:")
print("Get average loan amount by bucket")
print("Hint: Use .values('bucket').annotate(avg_amount=Avg('total_loan_amount'))")

# Write your answer here:
# avg_by_bucket = 


# QUESTION 19: String Operations
print("\n📝 QUESTION 19:")
print("Find customers whose names start with 'A' or 'B'")
print("Hint: Use Q objects with __istartswith")

# Write your answer here:
# customers_ab = 


# QUESTION 20: Exists Check
print("\n📝 QUESTION 20:")
print("Check if any allocation file has error records > 0")
print("Hint: Use .filter().exists()")

# Write your answer here:
# has_errors = 


print("\n" + "="*60)
print("🎯 PRACTICE SESSION 3: ADVANCED LEVEL (10 Questions)")
print("="*60)

# QUESTION 21: Complex Aggregation
print("\n📝 QUESTION 21:")
print("Get monthly case creation statistics for current year")
print("Hint: Use __year, __month with Count")

# Write your answer here:
# monthly_stats = 


# QUESTION 22: Conditional Expressions
print("\n📝 QUESTION 22:")
print("Mark cases as 'High Risk' if current_dpd > 60, else 'Low Risk'")
print("Hint: Use Case() and When() expressions")

# Write your answer here:
# risk_annotated = 


# QUESTION 23: Subquery
print("\n📝 QUESTION 23:")
print("Find users handling cases with above-average loan amounts")
print("Hint: Use Subquery with average calculation")

# Write your answer here:
# high_value_handlers = 


# QUESTION 24: Multiple Aggregations
print("\n📝 QUESTION 24:")
print("Get total, average, max, and min loan amounts for each process")
print("Hint: Use multiple aggregation functions")

# Write your answer here:
# process_stats = 


# QUESTION 25: Date Calculations
print("\n📝 QUESTION 25:")
print("Find cases where due date is within next 7 days")
print("Hint: Use date range with timezone.now()")

# Write your answer here:
# upcoming_due = 


# QUESTION 26: Performance Optimization
print("\n📝 QUESTION 26:")
print("Efficiently get case details with bucket and allocation file info")
print("Hint: Use select_related() for foreign keys")

# Write your answer here:
# optimized_cases = 


# QUESTION 27: Complex Business Logic
print("\n📝 QUESTION 27:")
print("Find potential duplicate customers (same phone number)")
print("Hint: Use values() and annotate() with Count")

# Write your answer here:
# potential_duplicates = 


# QUESTION 28: Mathematical Operations
print("\n📝 QUESTION 28:")
print("Calculate collection efficiency (last_payment_amount / minimum_due_amount)")
print("Hint: Use F() expressions for field calculations")

# Write your answer here:
# collection_efficiency = 


# QUESTION 29: Advanced Filtering
print("\n📝 QUESTION 29:")
print("Find users assigned to regions with more than 100 cases")
print("Hint: Use nested queries or annotations")

# Write your answer here:
# busy_region_users = 


# QUESTION 30: Data Analytics
print("\n📝 QUESTION 30:")
print("Create a comprehensive dashboard query with key metrics")
print("Hint: Combine multiple aggregations and annotations")

# Write your answer here:
# dashboard_data = 


print("\n" + "="*60)
print("🎯 TESTING YOUR SOLUTIONS")
print("="*60)

def test_solution(question_num, your_query, description):
    """
    Test your query solutions
    """
    print(f"\n🧪 Testing Question {question_num}: {description}")
    try:
        # Uncomment when you have models imported
        # result = your_query
        # print(f"✅ Query executed successfully!")
        # print(f"📊 Result type: {type(result)}")
        # if hasattr(result, 'count'):
        #     print(f"📈 Count: {result.count()}")
        print("⚠️  Uncomment model imports to test")
    except Exception as e:
        print(f"❌ Error: {e}")

# Example usage (uncomment when ready):
# test_solution(1, active_users, "Get all active users")

print("\n" + "="*60)
print("📚 LEARNING RESOURCES")
print("="*60)

learning_tips = """
🎯 PRACTICE TIPS:

1. 🏃‍♂️ START SMALL: Begin with Questions 1-10, master the basics
2. 🧪 USE DJANGO SHELL: Test your queries interactively
   python manage.py shell
3. 🔍 CHECK SQL: Use str(queryset.query) to see generated SQL
4. 📈 PROFILE QUERIES: Use Django Debug Toolbar
5. 📖 READ DOCS: Django QuerySet API reference
6. 🤝 ASK QUESTIONS: Don't hesitate to seek help

🚀 NEXT STEPS:
- Complete all 30 questions above
- Test your solutions with real data
- Move to more complex business scenarios
- Practice query optimization techniques

💡 COMMON PATTERNS IN YOUR SYSTEM:
- Regional hierarchy queries (Region → Zone → City → Pincode → Area)
- FO assignment based on geographical mapping
- Risk assessment and bucket categorization
- Collection efficiency and performance metrics
- Case lifecycle management and tracking
"""

print(learning_tips)

print("\n" + "="*60)
print("🎉 READY TO START? Begin with Question 1!")
print("="*60)