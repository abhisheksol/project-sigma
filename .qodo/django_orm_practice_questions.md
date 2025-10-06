# Django ORM Practice Questions - Sigma Sync Technologies Models
## 200 Questions from Beginner to Expert Level

Based on your models: LoanConfigurationsProcessModel, RegionConfigurationModels, UserModel, AllocationFileModel, CaseManagementCaseModel, and related models.

---

## **BEGINNER LEVEL (Questions 1-50)**

### Basic Queries & Filtering

**1.** Get all loan processes from LoanConfigurationsProcessModel
```python
# Your answer here
```

**2.** Count the total number of users in UserModel
```python
# Your answer here
```

**3.** Get all active users (is_active=True)
```python
# Your answer here
```

**4.** Find all regions with title containing "North"
```python
# Your answer here
```

**5.** Get all products where title is exactly "Personal Loan"
```python
# Your answer here
```

**6.** Retrieve all users who are staff members
```python
# Your answer here
```

**7.** Find all allocation files created in the last 30 days
```python
# Your answer here
```

**8.** Get all case management records with current_dpd greater than 30
```python
# Your answer here
```

**9.** Find all users with phone numbers starting with "9"
```python
# Your answer here
```

**10.** Get all bucket ranges where value is "0-30"
```python
# Your answer here
```

### Basic Field Lookups

**11.** Find all processes where contact_person_email is null
```python
# Your answer here
```

**12.** Get users created after January 1, 2024
```python
# Your answer here
```

**13.** Find all cases where customer_name starts with "John"
```python
# Your answer here
```

**14.** Get all regions where description is not null
```python
# Your answer here
```

**15.** Find users whose email contains "@gmail.com"
```python
# Your answer here
```

**16.** Get all allocation files where no_of_error_records is 0
```python
# Your answer here
```

**17.** Find all cases with loan_account_number ending with "001"
```python
# Your answer here
```

**18.** Get all users who are superusers
```python
# Your answer here
```

**19.** Find all products with description length greater than 50 characters
```python
# Your answer here
```

**20.** Get all zones belonging to a specific region (region_id = 'some-uuid')
```python
# Your answer here
```

### Basic Ordering & Limiting

**21.** Get the first 10 users ordered by username
```python
# Your answer here
```

**22.** Find the latest 5 allocation files by created_date
```python
# Your answer here
```

**23.** Get all processes ordered by title in descending order
```python
# Your answer here
```

**24.** Find the oldest user by created_date
```python
# Your answer here
```

**25.** Get the top 3 cases with highest total_loan_amount
```python
# Your answer here
```

**26.** Find all regions ordered by title alphabetically
```python
# Your answer here
```

**27.** Get the last login user (by last_login field)
```python
# Your answer here
```

**28.** Find 5 random users
```python
# Your answer here
```

**29.** Get all cities ordered by zone, then by city_name
```python
# Your answer here
```

**30.** Find the allocation file with maximum no_of_total_records
```python
# Your answer here
```

### Basic Field Selection

**31.** Get only usernames and emails of all users
```python
# Your answer here
```

**32.** Retrieve only title and description of all processes
```python
# Your answer here
```

**33.** Get id and customer_name of all cases
```python
# Your answer here
```

**34.** Fetch only title and value from bucket ranges
```python
# Your answer here
```

**35.** Get login_id and is_active status of all users
```python
# Your answer here
```

**36.** Retrieve only file URLs from allocation files
```python
# Your answer here
```

**37.** Get pincode values from all RegionConfigurationPincodeModel records
```python
# Your answer here
```

**38.** Fetch only title and icons from user roles
```python
# Your answer here
```

**39.** Get customer_name and primary_number from all cases
```python
# Your answer here
```

**40.** Retrieve only email and phone_number from users
```python
# Your answer here
```

### Basic Existence Checks

**41.** Check if a user with specific login_id exists
```python
# Your answer here
```

**42.** Verify if any allocation file has error records
```python
# Your answer here
```

**43.** Check if there are any inactive users
```python
# Your answer here
```

**44.** Verify if a specific CRN number exists in cases
```python
# Your answer here
```

**45.** Check if any process has a logo URL
```python
# Your answer here
```

**46.** Verify if there are users without phone numbers
```python
# Your answer here
```

**47.** Check if any case has alternate phone numbers
```python
# Your answer here
```

**48.** Verify if there are any expired allocation files
```python
# Your answer here
```

**49.** Check if any user has emergency contact details
```python
# Your answer here
```

**50.** Verify if there are any cases with penalty amounts
```python
# Your answer here
```

---

## **INTERMEDIATE LEVEL (Questions 51-120)**

### Foreign Key Relationships & Joins

**51.** Get all zones with their region titles
```python
# Your answer here
```

**52.** Find all users with their role titles
```python
# Your answer here
```

**53.** Get all cases with their bucket titles
```python
# Your answer here
```

**54.** Retrieve all cities with their zone and region information
```python
# Your answer here
```

**55.** Find all allocation files with their cycle and product assignment details
```python
# Your answer here
```

**56.** Get all product assignments with process and product titles
```python
# Your answer here
```

**57.** Find all user details with their assigned regions
```python
# Your answer here
```

**58.** Get all cases with their allocation file information
```python
# Your answer here
```

**59.** Retrieve all pincodes with their city, zone, and region details
```python
# Your answer here
```

**60.** Find all areas with their complete geographical hierarchy
```python
# Your answer here
```

### Reverse Foreign Key Queries

**61.** Get a region with all its zones
```python
# Your answer here
```

**62.** Find a user with all their assigned products
```python
# Your answer here
```

**63.** Get a process with all its product assignments
```python
# Your answer here
```

**64.** Find an allocation file with all its cases
```python
# Your answer here
```

**65.** Get a bucket with all its associated cases
```python
# Your answer here
```

**66.** Find a cycle with all allocation files using it
```python
# Your answer here
```

**67.** Get a user role with all users having that role
```python
# Your answer here
```

**68.** Find a city with all its pincodes
```python
# Your answer here
```

**69.** Get a zone with all its cities and their pincodes
```python
# Your answer here
```

**70.** Find a product with all its assignments
```python
# Your answer here
```

### Many-to-Many Relationships

**71.** Get all users assigned to a specific region
```python
# Your answer here
```

**72.** Find all regions assigned to a specific user
```python
# Your answer here
```

**73.** Get users assigned to multiple zones
```python
# Your answer here
```

**74.** Find all cities assigned to a specific user
```python
# Your answer here
```

**75.** Get users with no regional assignments
```python
# Your answer here
```

**76.** Find users assigned to both pincodes and areas
```python
# Your answer here
```

**77.** Get all areas assigned to users in a specific city
```python
# Your answer here
```

**78.** Find users assigned to more than 5 pincodes
```python
# Your answer here
```

**79.** Get regions that have no assigned users
```python
# Your answer here
```

**80.** Find users assigned to areas in multiple pincodes
```python
# Your answer here
```

### Complex Filtering with Q Objects

**81.** Find users who are either staff or superuser
```python
# Your answer here
```

**82.** Get cases where customer_name contains "Singh" OR primary_number starts with "9"
```python
# Your answer here
```

**83.** Find allocation files with either high error count OR high duplicate count
```python
# Your answer here
```

**84.** Get users who are active AND (verified OR approved)
```python
# Your answer here
```

**85.** Find cases where total_loan_amount > 100000 OR current_dpd > 90
```python
# Your answer here
```

**86.** Get processes where contact email is provided OR contact phone is provided
```python
# Your answer here
```

**87.** Find users with role "Manager" OR "Senior Manager"
```python
# Your answer here
```

**88.** Get cases where customer has PAN number AND Aadhar number (if exists)
```python
# Your answer here
```

**89.** Find allocation files created this month OR last month
```python
# Your answer here
```

**90.** Get users who are NOT (inactive AND unverified)
```python
# Your answer here
```

### Aggregations

**91.** Count total number of cases per bucket
```python
# Your answer here
```

**92.** Get average loan amount by bucket
```python
# Your answer here
```

**93.** Find total EMI amount collected per region
```python
# Your answer here
```

**94.** Calculate sum of total_loan_amount for each process
```python
# Your answer here
```

**95.** Get maximum and minimum DPD values
```python
# Your answer here
```

**96.** Count users by role
```python
# Your answer here
```

**97.** Calculate average allocation file size (total records) per cycle
```python
# Your answer here
```

**98.** Get total penalty amount by city
```python
# Your answer here
```

**99.** Find the process with most product assignments
```python
# Your answer here
```

**100.** Calculate success rate of allocation files (valid/total records)
```python
# Your answer here
```

### Date and Time Queries

**101.** Get cases created in the last 7 days
```python
# Your answer here
```

**102.** Find users who logged in this week
```python
# Your answer here
```

**103.** Get allocation files expiring in next 30 days
```python
# Your answer here
```

**104.** Find cases where due_date is tomorrow
```python
# Your answer here
```

**105.** Get users created in current month
```python
# Your answer here
```

**106.** Find cases where last_payment_date is more than 60 days ago
```python
# Your answer here
```

**107.** Get allocation files created on weekends
```python
# Your answer here
```

**108.** Find cases with loan_disbursement_date in 2023
```python
# Your answer here
```

**109.** Get users who never logged in
```python
# Your answer here
```

**110.** Find overdue cases (due_date < today)
```python
# Your answer here
```

### Conditional Expressions

**111.** Annotate users with "Senior" or "Junior" based on created_date
```python
# Your answer here
```

**112.** Mark cases as "High Risk" if current_dpd > 60, else "Low Risk"
```python
# Your answer here
```

**113.** Categorize loan amounts as "Small", "Medium", or "Large"
```python
# Your answer here
```

**114.** Mark allocation files as "Clean" or "Problematic" based on error count
```python
# Your answer here
```

**115.** Categorize users by their last login (Recent, Old, Never)
```python
# Your answer here
```

**116.** Mark cases as "Overdue" or "Current" based on due_date
```python
# Your answer here
```

**117.** Categorize EMI amounts into ranges (Low, Medium, High)
```python
# Your answer here
```

**118.** Mark users as "Complete Profile" or "Incomplete" based on filled fields
```python
# Your answer here
```

**119.** Categorize regions by number of assigned users
```python
# Your answer here
```

**120.** Mark processes as "Active" or "Inactive" based on recent allocation files
```python
# Your answer here
```

---

## **ADVANCED LEVEL (Questions 121-170)**

### Complex Aggregations with Grouping

**121.** Get monthly case creation statistics for the last year
```python
# Your answer here
```

**122.** Calculate collection efficiency by region and month
```python
# Your answer here
```

**123.** Find average DPD progression by bucket over time
```python
# Your answer here
```

**124.** Get user productivity metrics (cases handled per user per month)
```python
# Your answer here
```

**125.** Calculate allocation file success rates by process and product
```python
# Your answer here
```

**126.** Find regional performance metrics (collection vs. allocation)
```python
# Your answer here
```

**127.** Get bucket migration patterns (cases moving between buckets)
```python
# Your answer here
```

**128.** Calculate user workload distribution across regions
```python
# Your answer here
```

**129.** Find seasonal trends in loan disbursements
```python
# Your answer here
```

**130.** Get process-wise risk distribution
```python
# Your answer here
```

### Window Functions & Advanced Analytics

**131.** Rank users by total loan amount handled (dense_rank)
```python
# Your answer here
```

**132.** Get running total of cases created per day
```python
# Your answer here
```

**133.** Calculate percentage of cases per bucket (over total)
```python
# Your answer here
```

**134.** Find top 3 users by collection amount in each region
```python
# Your answer here
```

**135.** Get moving average of DPD over last 30 days
```python
# Your answer here
```

**136.** Calculate case resolution rate by user with ranking
```python
# Your answer here
```

**137.** Find lag between allocation file creation and first case creation
```python
# Your answer here
```

**138.** Get percentile distribution of loan amounts
```python
# Your answer here
```

**139.** Calculate cumulative collection amount by region
```python
# Your answer here
```

**140.** Find users with improving/declining performance trends
```python
# Your answer here
```

### Complex Subqueries

**141.** Find users handling cases with highest average loan amounts
```python
# Your answer here
```

**142.** Get regions with above-average case resolution rates
```python
# Your answer here
```

**143.** Find processes with allocation files having zero errors
```python
# Your answer here
```

**144.** Get users assigned to regions with highest case volumes
```python
# Your answer here
```

**145.** Find cases belonging to most productive allocation files
```python
# Your answer here
```

**146.** Get buckets containing cases from multiple processes
```python
# Your answer here
```

**147.** Find users with assignments in regions having specific criteria
```python
# Your answer here
```

**148.** Get allocation files from cycles with highest success rates
```python
# Your answer here
```

**149.** Find cases with loan amounts above process average
```python
# Your answer here
```

**150.** Get regions where all assigned users are active
```python
# Your answer here
```

### Performance Optimization Queries

**151.** Optimize query to get case details with minimal database hits
```python
# Your answer here
```

**152.** Use select_related for user role and region information
```python
# Your answer here
```

**153.** Prefetch related data for user assignments efficiently
```python
# Your answer here
```

**154.** Optimize allocation file queries with case counts
```python
# Your answer here
```

**155.** Use only() and defer() for large case management queries
```python
# Your answer here
```

**156.** Create efficient query for geographical hierarchy display
```python
# Your answer here
```

**157.** Optimize user dashboard data retrieval
```python
# Your answer here
```

**158.** Use database functions for date calculations instead of Python
```python
# Your answer here
```

**159.** Create efficient pagination for large case lists
```python
# Your answer here
```

**160.** Optimize search queries across multiple fields
```python
# Your answer here
```

### Custom Managers and QuerySets

**161.** Create custom manager for active users only
```python
# Your answer here
```

**162.** Build custom queryset for overdue cases
```python
# Your answer here
```

**163.** Create manager method for geographical hierarchy queries
```python
# Your answer here
```

**164.** Build custom queryset for allocation file statistics
```python
# Your answer here
```

**165.** Create manager for user productivity metrics
```python
# Your answer here
```

**166.** Build custom queryset for risk-based case filtering
```python
# Your answer here
```

**167.** Create manager for regional performance analytics
```python
# Your answer here
```

**168.** Build custom queryset for loan lifecycle tracking
```python
# Your answer here
```

**169.** Create manager for collection efficiency metrics
```python
# Your answer here
```

**170.** Build custom queryset for process-wise reporting
```python
# Your answer here
```

---

## **EXPERT LEVEL (Questions 171-200)**

### Complex Business Logic Queries

**171.** Create a query to identify potential fraud cases based on multiple criteria
```python
# Hint: Consider duplicate phone numbers, unusual loan patterns, rapid applications
```

**172.** Build a sophisticated FO assignment algorithm query
```python
# Hint: Consider distance, workload, performance, availability
```

**173.** Create a query for dynamic risk scoring based on historical data
```python
# Hint: Payment history, DPD trends, demographic factors
```

**174.** Build a collection prioritization engine query
```python
# Hint: Amount, DPD, customer profile, historical success rate
```

**175.** Create a query for optimal route planning for field officers
```python
# Hint: Geographical clustering, case priorities, time constraints
```

**176.** Build a customer segmentation query based on behavior patterns
```python
# Hint: Payment patterns, loan types, demographic clustering
```

**177.** Create a predictive query for case escalation probability
```python
# Hint: Historical patterns, current status, external factors
```

**178.** Build a query for automated bucket migration suggestions
```python
# Hint: DPD progression, payment patterns, risk factors
```

**179.** Create a comprehensive portfolio health assessment query
```python
# Hint: Multiple KPIs, trend analysis, comparative metrics
```

**180.** Build a query for intelligent allocation file validation
```python
# Hint: Data consistency, business rules, historical patterns
```

### Advanced Reporting & Analytics

**181.** Create a management dashboard query with all key metrics
```python
# Multiple aggregations, trends, comparisons
```

**182.** Build a regulatory compliance reporting query
```python
# Audit trails, data quality, completeness checks
```

**183.** Create a performance benchmarking query across regions
```python
# Comparative analysis, statistical measures
```

**184.** Build a customer lifecycle value analysis query
```python
# Revenue, costs, lifetime predictions
```

**185.** Create a risk portfolio analysis query
```python
# Concentration risks, diversification metrics
```

**186.** Build a collection effectiveness analysis query
```python
# Success rates, cost per collection, ROI metrics
```

**187.** Create a geographical market analysis query
```python
# Market penetration, growth opportunities
```

**188.** Build a product performance comparison query
```python
# Cross-product metrics, profitability analysis
```

**189.** Create a seasonal business pattern analysis query
```python
# Time series analysis, seasonal adjustments
```

**190.** Build a competitive positioning analysis query
```python
# Market share, performance comparisons
```

### System Integration & Data Migration

**191.** Create a data migration validation query
```python
# Data integrity, completeness, consistency checks
```

**192.** Build a query for external system synchronization
```python
# Change detection, delta updates, conflict resolution
```

**193.** Create a data quality assessment query
```python
# Completeness, accuracy, consistency metrics
```

**194.** Build a query for automated data cleansing suggestions
```python
# Pattern detection, anomaly identification
```

**195.** Create a system performance monitoring query
```python
# Query performance, data growth, system health
```

**196.** Build a query for backup and recovery validation
```python
# Data consistency, completeness verification
```

**197.** Create a multi-tenant data isolation query
```python
# Security, data segregation, access control
```

**198.** Build a query for automated testing data generation
```python
# Realistic test data, referential integrity
```

**199.** Create a comprehensive system audit query
```python
# All activities, changes, user actions
```

**200.** Build the ultimate master query combining all business requirements
```python
# Integration of all modules, complete business view
```

---

## **Answer Key Structure**

For each question, provide:
1. **Query Solution** - The actual Django ORM code
2. **Explanation** - Why this approach is used
3. **Performance Notes** - Any optimization considerations
4. **Business Context** - How this relates to your loan management system
5. **Alternative Approaches** - Other ways to solve the same problem

---

## **Practice Tips**

1. **Start with the basics** - Master simple queries before moving to complex ones
2. **Use Django shell** - Test your queries interactively
3. **Check SQL output** - Use `str(queryset.query)` to see generated SQL
4. **Profile your queries** - Use Django Debug Toolbar or similar tools
5. **Understand your data** - Know the relationships and constraints
6. **Practice regularly** - Set aside time daily for ORM practice
7. **Read Django documentation** - Stay updated with new features
8. **Join Django communities** - Learn from others' experiences

---

## **Resources for Further Learning**

- Django ORM Documentation
- Django QuerySet API Reference
- Database optimization guides
- SQL to Django ORM conversion tools
- Django debugging tools

Happy practicing! 🚀