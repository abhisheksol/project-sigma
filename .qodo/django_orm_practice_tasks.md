# Django ORM Practice Tasks - Sigma Sync Technologies
## 100+ Practical Questions for Hands-On Practice

Based on your loan management system models. Each question includes the task and expected Django ORM solution.

---

## **BASIC LEVEL (Tasks 1-25)**

### Region Configuration Tasks

**1. Print all region data**
```python
# Task: Display all regions with their titles and descriptions
# Expected output: List of all regions

# Your solution:
regions = RegionConfigurationRegionModel.objects.all()
for region in regions:
    print(f"Region: {region.title}, Description: {region.description}")
```

**2. Create a new region**
```python
# Task: Create a region named "North Zone" with description "Northern region operations"

# Your solution:
```

**3. Find regions by title pattern**
```python
# Task: Find all regions whose title contains "Central"

# Your solution:
```

**4. Get all zones for a specific region**
```python
# Task: Get all zones belonging to region with title "West Zone"

# Your solution:
```

**5. Create a complete geographical hierarchy**
```python
# Task: Create Region -> Zone -> City -> Pincode -> Area hierarchy
# Region: "Mumbai Region"
# Zone: "South Mumbai"  
# City: "Mumbai"
# Pincode: "400001"
# Area: "Fort"

# Your solution:
```

### User Management Tasks

**6. Create users hierarchically**
```python
# Task: Create user hierarchy: Admin -> Senior Manager -> Manager -> Field Officer
# Admin: login_id="admin001", email="admin@sigma.com"
# Sr Manager: login_id="sm001", reports_to=admin
# Manager: login_id="mgr001", reports_to=sr_manager  
# FO: login_id="fo001", reports_to=manager

# Your solution:
```

**7. Find all active users**
```python
# Task: Get all users where is_active=True and is_verified=True

# Your solution:
```

**8. Get user's reporting hierarchy**
```python
# Task: For a given user, show their complete reporting chain (who they report to)

# Your solution:
```

**9. Find users by role**
```python
# Task: Get all users with role "Field Officer"

# Your solution:
```

**10. Create user with profile details**
```python
# Task: Create a user and their UserDetailModel with emergency contact info
# User: login_id="fo002", email="fo002@sigma.com"
# Details: blood_group="O+", emergency_phone="9876543210"

# Your solution:
```

### Process & Product Configuration

**11. Create a loan process**
```python
# Task: Create a process for "HDFC Bank" with contact person details
# title="HDFC Bank", contact_person_name="John Doe", contact_person_email="john@hdfc.com"

# Your solution:
```

**12. Create products for a process**
```python
# Task: Create 3 products: "Personal Loan", "Home Loan", "Car Loan" 

# Your solution:
```

**13. Assign products to process**
```python
# Task: Create product assignments linking HDFC Bank to all 3 loan products
# Set min_due_percentage=10.0, refer_back_percentage=5.0

# Your solution:
```

**14. Create bucket configuration**
```python
# Task: Create bucket ranges and buckets
# Ranges: "0-30", "31-60", "61-90", "90+"
# Buckets: "Bucket 1", "Bucket 2", "Bucket 3", "Bucket 4"

# Your solution:
```

**15. Find all processes with their products**
```python
# Task: Display all processes and their assigned products

# Your solution:
```

### Basic Filtering & Searching

**16. Search users by phone number**
```python
# Task: Find users whose phone number starts with "98"

# Your solution:
```

**17. Find recently created records**
```python
# Task: Get all users created in the last 7 days

# Your solution:
```

**18. Get empty/null field records**
```python
# Task: Find all processes where contact_person_email is null or empty

# Your solution:
```

**19. Count records by category**
```python
# Task: Count total users, processes, products, and regions

# Your solution:
```

**20. Find duplicate phone numbers**
```python
# Task: Find users who have the same phone number

# Your solution:
```

### Basic User Assignments

**21. Assign regions to user**
```python
# Task: Assign 2 regions to a Senior Manager

# Your solution:
```

**22. Assign zones to user**
```python
# Task: Assign 3 zones to a Manager

# Your solution:
```

**23. Assign pincodes to field officer**
```python
# Task: Assign 5 pincodes to a Field Officer for their area coverage

# Your solution:
```

**24. Find users without assignments**
```python
# Task: Find all users who have no regional assignments

# Your solution:
```

**25. Get user's assigned areas**
```python
# Task: For a specific user, show all their assigned regions, zones, cities, pincodes, and areas

# Your solution:
```

---

## **INTERMEDIATE LEVEL (Tasks 26-60)**

### Allocation File Management

**26. Create an allocation file**
```python
# Task: Create allocation file with cycle, product assignment, and record counts
# title="HDFC_Personal_Loan_Oct2024", no_of_total_records=1000, no_of_valid_records=950

# Your solution:
```

**27. Calculate allocation file statistics**
```python
# Task: For each allocation file, calculate success rate (valid/total records)

# Your solution:
```

**28. Find problematic allocation files**
```python
# Task: Find allocation files where error_records > 10% of total_records

# Your solution:
```

**29. Get allocation files by date range**
```python
# Task: Get all allocation files created between two specific dates

# Your solution:
```

**30. Update allocation file status**
```python
# Task: Update latest_reupload_file_url for a specific allocation file

# Your solution:
```

### Case Management Tasks

**31. Create a loan case**
```python
# Task: Create a complete case with customer details, loan info, and address
# customer_name="Rajesh Kumar", primary_number="9876543210"
# loan_account_number="HDFC123456", total_loan_amount=500000

# Your solution:
```

**32. Find overdue cases**
```python
# Task: Find all cases where due_date < today

# Your solution:
```

**33. Get high-risk cases**
```python
# Task: Find cases with current_dpd > 60 and total_loan_amount > 100000

# Your solution:
```

**34. Calculate bucket-wise statistics**
```python
# Task: Count cases and sum loan amounts for each bucket

# Your solution:
```

**35. Find cases by customer pattern**
```python
# Task: Find cases where customer_name contains "Kumar" or "Singh"

# Your solution:
```

**36. Update case status**
```python
# Task: Update case status and disposition for multiple cases

# Your solution:
```

**37. Find cases with missing information**
```python
# Task: Find cases where alternate_number_1 is null but alternate_number_2 is not null

# Your solution:
```

**38. Get monthly case creation trend**
```python
# Task: Count cases created each month for the current year

# Your solution:
```

**39. Find cases by geographical location**
```python
# Task: Find all cases in a specific city or pincode

# Your solution:
```

**40. Calculate collection statistics**
```python
# Task: Calculate total collectable_amount by bucket and region

# Your solution:
```

### Advanced Filtering & Joins

**41. Get users with their complete hierarchy**
```python
# Task: Show users with their role, manager, and all reportees

# Your solution:
```

**42. Find cross-regional assignments**
```python
# Task: Find users assigned to areas in multiple different regions

# Your solution:
```

**43. Get process performance metrics**
```python
# Task: For each process, show total allocation files, total cases, success rate

# Your solution:
```

**44. Find geographical coverage gaps**
```python
# Task: Find pincodes that have no assigned field officers

# Your solution:
```

**45. Get user workload distribution**
```python
# Task: Show case count and total loan amount per assigned user

# Your solution:
```

**46. Find allocation file dependencies**
```python
# Task: Show which cases belong to which allocation files and their status

# Your solution:
```

**47. Get regional performance comparison**
```python
# Task: Compare collection amounts and case counts across regions

# Your solution:
```

**48. Find product-wise risk distribution**
```python
# Task: Show risk distribution (High/Medium/Low) for each product type

# Your solution:
```

**49. Get time-based user activity**
```python
# Task: Show user login patterns and case handling over time

# Your solution:
```

**50. Find relationship inconsistencies**
```python
# Task: Find cases assigned to allocation files from different processes

# Your solution:
```

### Aggregation & Reporting Tasks

**51. Create daily dashboard data**
```python
# Task: Get today's key metrics: new cases, collections, overdue count

# Your solution:
```

**52. Generate monthly report**
```python
# Task: Monthly summary by region: cases, collections, resolution rate

# Your solution:
```

**53. Calculate user performance metrics**
```python
# Task: For each user, calculate: cases handled, avg resolution time, success rate

# Your solution:
```

**54. Get bucket migration analysis**
```python
# Task: Analyze how cases move between buckets over time

# Your solution:
```

**55. Find top performing processes**
```python
# Task: Rank processes by collection efficiency and case volume

# Your solution:
```

**56. Calculate geographical metrics**
```python
# Task: Show case density and collection amounts by city/pincode

# Your solution:
```

**57. Get product profitability analysis**
```python
# Task: Calculate revenue vs. collection costs for each product

# Your solution:
```

**58. Find seasonal patterns**
```python
# Task: Analyze case creation and collection patterns by month/quarter

# Your solution:
```

**59. Get risk assessment summary**
```python
# Task: Risk distribution analysis across different dimensions

# Your solution:
```

**60. Create management summary report**
```python
# Task: Executive summary with all key business metrics

# Your solution:
```

---

## **ADVANCED LEVEL (Tasks 61-85)**

### Complex Business Logic

**61. Implement FO assignment algorithm**
```python
# Task: Assign cases to field officers based on:
# - Pincode proximity (assigned areas)
# - Current workload (case count)
# - Performance rating
# - Availability status

# Your solution:
```

**62. Create dynamic risk scoring**
```python
# Task: Calculate risk score based on:
# - Current DPD (weight: 40%)
# - Loan amount (weight: 30%)
# - Payment history (weight: 20%)
# - Customer profile (weight: 10%)

# Your solution:
```

**63. Build collection prioritization engine**
```python
# Task: Prioritize cases for collection based on:
# - Recovery potential (amount vs. effort)
# - Days past due
# - Historical success rate for similar profiles
# - Geographic efficiency

# Your solution:
```

**64. Implement route optimization logic**
```python
# Task: Group cases by geographical proximity for efficient field visits
# Consider: distance, case priority, time constraints

# Your solution:
```

**65. Create fraud detection system**
```python
# Task: Identify potential fraud cases by finding:
# - Multiple cases with same phone number
# - Similar addresses with different customers
# - Unusual application patterns

# Your solution:
```

**66. Build customer segmentation**
```python
# Task: Segment customers based on:
# - Payment behavior (Regular/Irregular/Defaulter)
# - Loan size (Small/Medium/Large)
# - Geographic location
# - Product type

# Your solution:
```

**67. Implement escalation rules**
```python
# Task: Auto-escalate cases based on:
# - DPD thresholds
# - Amount thresholds
# - Failed contact attempts
# - Manager availability

# Your solution:
```

**68. Create performance benchmarking**
```python
# Task: Compare FO performance against:
# - Regional averages
# - Historical performance
# - Peer comparisons
# - Target achievements

# Your solution:
```

**69. Build capacity planning model**
```python
# Task: Calculate required FO capacity based on:
# - Case volume projections
# - Average cases per FO
# - Geographic coverage requirements
# - Seasonal variations

# Your solution:
```

**70. Implement collection strategy optimizer**
```python
# Task: Suggest optimal collection strategy based on:
# - Customer profile
# - Historical success rates
# - Cost-benefit analysis
# - Resource availability

# Your solution:
```

### Advanced Reporting & Analytics

**71. Create cohort analysis**
```python
# Task: Analyze loan performance by disbursement cohorts
# Track: Default rates, collection rates, lifecycle patterns

# Your solution:
```

**72. Build predictive analytics**
```python
# Task: Predict case resolution probability based on historical data

# Your solution:
```

**73. Generate compliance reports**
```python
# Task: Create reports for regulatory compliance:
# - Data completeness
# - Process adherence
# - SLA compliance

# Your solution:
```

**74. Implement portfolio risk analysis**
```python
# Task: Analyze portfolio risk across multiple dimensions:
# - Geographic concentration
# - Product concentration
# - Vintage analysis

# Your solution:
```

**75. Create operational efficiency metrics**
```python
# Task: Calculate operational KPIs:
# - Cost per case
# - Resolution time
# - Resource utilization
# - Process efficiency

# Your solution:
```

### Data Integration & Migration

**76. Build data validation framework**
```python
# Task: Validate data consistency across all models:
# - Referential integrity
# - Business rule compliance
# - Data quality checks

# Your solution:
```

**77. Create data synchronization logic**
```python
# Task: Sync data changes across related models:
# - User assignments
# - Case updates
# - Status propagation

# Your solution:
```

**78. Implement audit trail system**
```python
# Task: Track all changes to critical data:
# - Who changed what and when
# - Before/after values
# - Business justification

# Your solution:
```

**79. Build data archival process**
```python
# Task: Archive old data based on:
# - Retention policies
# - Case closure dates
# - Regulatory requirements

# Your solution:
```

**80. Create data quality monitoring**
```python
# Task: Monitor data quality metrics:
# - Completeness scores
# - Accuracy measures
# - Consistency checks

# Your solution:
```

**81. Implement backup validation**
```python
# Task: Validate backup data integrity:
# - Record counts
# - Checksum validation
# - Relationship verification

# Your solution:
```

**82. Build data migration utilities**
```python
# Task: Create utilities for data migration:
# - Format conversion
# - Data mapping
# - Error handling

# Your solution:
```

**83. Create system health monitoring**
```python
# Task: Monitor system health:
# - Query performance
# - Data growth rates
# - Resource utilization

# Your solution:
```

**84. Implement change management**
```python
# Task: Track and manage schema/data changes:
# - Version control
# - Impact analysis
# - Rollback procedures

# Your solution:
```

**85. Build comprehensive testing framework**
```python
# Task: Create automated tests for:
# - Data integrity
# - Business logic
# - Performance benchmarks

# Your solution:
```

---

## **EXPERT LEVEL (Tasks 86-105)**

### Master-Level Integration Tasks

**86. Build complete loan origination workflow**
```python
# Task: Create end-to-end loan processing:
# Customer application -> Credit check -> Approval -> Disbursement -> Case creation

# Your solution:
```

**87. Implement AI-powered FO assignment**
```python
# Task: Use machine learning for optimal FO assignment:
# - Historical success patterns
# - Geographic optimization  
# - Workload balancing
# - Performance prediction

# Your solution:
```

**88. Create real-time risk monitoring**
```python
# Task: Build real-time risk dashboard:
# - Portfolio risk metrics
# - Early warning indicators
# - Automated alerts
# - Trend analysis

# Your solution:
```

**89. Build dynamic pricing engine**
```python
# Task: Implement risk-based pricing:
# - Customer risk assessment
# - Market conditions
# - Competitive analysis
# - Profitability optimization

# Your solution:
```

**90. Create omnichannel communication system**
```python
# Task: Integrate communication across channels:
# - SMS, Email, Voice, WhatsApp
# - Customer preferences
# - Channel effectiveness
# - Cost optimization

# Your solution:
```

**91. Implement advanced analytics platform**
```python
# Task: Build comprehensive analytics:
# - Real-time dashboards
# - Predictive models
# - What-if scenarios
# - ROI calculators

# Your solution:
```

**92. Create intelligent case routing**
```python
# Task: Smart case distribution:
# - Skills-based routing
# - Workload optimization
# - Priority handling
# - Escalation management

# Your solution:
```

**93. Build collection optimization engine**
```python
# Task: Optimize collection strategies:
# - Customer behavior analysis
# - Channel effectiveness
# - Timing optimization
# - Message personalization

# Your solution:
```

**94. Implement regulatory compliance automation**
```python
# Task: Automate compliance processes:
# - Data privacy (GDPR/CCPA)
# - Financial regulations
# - Audit trail maintenance
# - Report generation

# Your solution:
```

**95. Create customer lifecycle management**
```python
# Task: Manage complete customer journey:
# - Acquisition to retention
# - Cross-selling opportunities
# - Churn prediction
# - Lifetime value optimization

# Your solution:
```

### Ultimate Integration Challenges

**96. Build enterprise data warehouse**
```python
# Task: Create comprehensive data warehouse:
# - Extract, Transform, Load (ETL)
# - Data modeling
# - Performance optimization
# - Historical data management

# Your solution:
```

**97. Implement microservices architecture**
```python
# Task: Design microservices for:
# - User management
# - Case processing
# - Notification service
# - Analytics engine

# Your solution:
```

**98. Create API ecosystem**
```python
# Task: Build RESTful APIs for:
# - Third-party integrations
# - Mobile applications
# - Partner systems
# - External data sources

# Your solution:
```

**99. Build disaster recovery system**
```python
# Task: Implement complete DR solution:
# - Data replication
# - Failover procedures
# - Recovery testing
# - Business continuity

# Your solution:
```

**100. Create AI-powered insights engine**
```python
# Task: Build ML-powered system for:
# - Predictive analytics
# - Anomaly detection
# - Recommendation engine
# - Natural language processing

# Your solution:
```

### Bonus Master Challenges

**101. Implement blockchain for audit trail**
```python
# Task: Use blockchain for immutable audit logging

# Your solution:
```

**102. Create IoT integration for asset tracking**
```python
# Task: Integrate IoT devices for vehicle/asset monitoring

# Your solution:
```

**103. Build quantum-resistant security**
```python
# Task: Implement advanced encryption for sensitive data

# Your solution:
```

**104. Create multi-tenant SaaS platform**
```python
# Task: Build platform for multiple financial institutions

# Your solution:
```

**105. Implement zero-downtime deployment**
```python
# Task: Blue-green deployment with data migration

# Your solution:
```

---

## **Practice Instructions**

### How to Practice:

1. **Set up Django shell**: `python manage.py shell`

2. **Import your models**:
```python
from store.configurations.loan_config.models import *
from store.configurations.region_config.models import *
from user_config.user_auth.models import *
from accounts.models import *
from store.operations.allocation_files.models import *
from store.operations.case_management.models import *
```

3. **Start with Task 1** and work your way up

4. **Test each solution** before moving to the next

5. **Time yourself** - aim to solve each task efficiently

6. **Document your solutions** for future reference

### Success Metrics:
- **Basic (1-25)**: Complete in 2-3 hours
- **Intermediate (26-60)**: Complete in 4-5 hours  
- **Advanced (61-85)**: Complete in 6-8 hours
- **Expert (86-105)**: Complete in 8-10 hours

### Tips:
- Use `print()` statements to verify your results
- Test with small datasets first
- Use Django Debug Toolbar to monitor query performance  
- Create sample data for testing
- Document complex queries with comments

**Happy practicing!** 🚀