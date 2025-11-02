# 📚 NBA Skins Project - Complete Documentation Index & Guide

## 🎯 Quick Start - Which Document Do You Need?

### 🚀 Starting a New Chat Session?
**→ Use: CHAT_HANDOFF_TEMPLATE.md**
- Pre-formatted for copy/paste into Claude
- Essential context without overwhelming detail
- Links to deeper documentation
- **Best for:** Continuing work in a fresh conversation

### ⚡ Need a Quick Answer?
**→ Use: QUICK_REFERENCE.md**
- ~200 lines of essential information
- Common issues & solutions
- Key code patterns
- Historical baseline data
- **Best for:** Looking up specific facts quickly

### 📖 Need Complete Understanding?
**→ Use: COMPLETE_PROJECT_DOCUMENTATION.md**
- ~400 lines of comprehensive detail
- All edge cases documented
- Full technical specifications
- Complete troubleshooting guide
- **Best for:** Deep understanding or major changes

---

## 📄 All Documentation Files (Organized by Purpose)

### 🎯 Core Documentation (Essential - Start Here)

#### 1. **CHAT_HANDOFF_TEMPLATE.md** ⭐
- **Purpose:** Handoff to new Claude chat session
- **When:** Opening fresh conversation
- **Key Features:**
  - Project overview in ~100 lines
  - Recent changes (Oct 31, 2025)
  - Critical fixes summary
  - How to continue work
- **Pro Tip:** Copy entire file, paste into new chat with "Continue working on this project"

#### 2. **QUICK_REFERENCE.md** ⭐
- **Purpose:** Fast lookup reference
- **When:** Need quick answer or refresh
- **Key Sections:**
  - Essential features summary
  - Historical baseline data (critical for YTD calculations)
  - Common issues & fixes
  - Key code patterns
  - Data source URLs
- **Pro Tip:** Keep open in second window while working

#### 3. **COMPLETE_PROJECT_DOCUMENTATION.md** ⭐
- **Purpose:** Comprehensive technical reference
- **When:** Major changes, debugging complex issues
- **Key Sections:**
  - Full project architecture
  - Every feature detailed
  - All edge cases
  - Complete troubleshooting
  - Development history
- **Pro Tip:** Search this first when encountering unfamiliar behavior

---

### 🔧 Fix Documentation (Recent Changes)

#### 4. **FIXES_SUMMARY.md**
- **What:** Oct 31, 2025 fixes overview
- **Contents:**
  - Night mode toggle fix
  - YTD data accuracy improvements
  - Before/after comparisons
  - Quick verification steps
- **When to Read:** Understanding recent changes

#### 5. **FIXES_APPLIED.md**
- **What:** Detailed technical explanations
- **Contents:**
  - Code changes made
  - Why changes were necessary
  - Verification checklist
  - Cleanup instructions
- **When to Read:** Debugging issues related to recent fixes

#### 6. **HYBRID_APPROACH_FIX.md**
- **What:** Yesterday's data solution
- **Contents:**
  - Problem: Scraping "today" gave wrong data for yesterday
  - Solution: Hybrid scraping + CSV approach
  - Benefits and tradeoffs
- **Key Insight:** Date-specific URLs required for historical accuracy

#### 7. **WON_SKIN_LOGIC_FIX.md**
- **What:** Correct skin calculation logic
- **Contents:**
  - Common misunderstanding about skin awards
  - Correct logic: (Won_Game=TRUE AND Pick="W") OR (Won_Game=FALSE AND Pick="L")
  - Example calculations
- **Critical:** This logic is used throughout the system

---

### 🎨 Feature Documentation

#### 8. **NEW_FEATURES_GUIDE.md**
- **What:** Guide to three major features
- **Contents:**
  - Historical data integration
  - Chart explanations (cumulative luck, expected skins)
  - Night mode usage
  - FAQ section
- **When to Read:** Understanding feature behavior

#### 9. **IMPLEMENTATION_SUMMARY.md**
- **What:** Technical implementation details
- **Contents:**
  - What was implemented
  - Code structure overview
  - Testing checklist
  - Success metrics
- **When to Read:** Understanding how features work technically

#### 10. **COMPLETE_VISUAL_GUIDE.md**
- **What:** Visual examples and layouts
- **Contents:**
  - Page layout diagrams
  - Chart visualizations
  - Dark mode comparisons
  - Data flow diagrams
- **When to Read:** Understanding visual aspects

#### 11. **COMPLETE_FEATURES.md**
- **What:** Final feature summary
- **Contents:**
  - All three major features
  - Expected results
  - Testing checklist
- **When to Read:** Final verification before deployment

---

### 🔍 Specialized Documentation

#### 12. **ERROR_FIX.md**
- **What:** Won_Game column error resolution
- **Problem:** Parsing issue with CSV data
- **Solution:** Correct column extraction logic

#### 13. **YESTERDAY_TABLE_ADDED.md**
- **What:** Yesterday's matchup table feature
- **Key Feature:** Head-to-head matchup display for previous day

#### 14. **YESTERDAY_FIX.md**
- **What:** Yesterday's scraping fix
- **Problem:** Generic scraping gave wrong results
- **Solution:** Date-specific URL scraping

#### 15. **TABLE_COMPARISON.md**
- **What:** Today vs Yesterday table differences
- **Why Useful:** Understand behavioral differences

---

### 📦 Legacy Documentation

#### 16. **FIX_NOTES.md, UPDATE_SUMMARY.md, VISUAL_GUIDE.md**
- **Status:** Superseded by newer docs
- **Note:** May contain outdated information
- **Keep?** Optional - for historical context only

---

## 🗂️ Recommended Reading Order by Use Case

### 🆕 For New Users (First Time Seeing Project)
1. **README.md** (this file) - Orientation
2. **QUICK_REFERENCE.md** - Get overview
3. **COMPLETE_PROJECT_DOCUMENTATION.md** - Deep dive
4. **NEW_FEATURES_GUIDE.md** - Understand features
5. **CHAT_HANDOFF_TEMPLATE.md** - For future reference

### 🔄 For Continuing Development (New Chat Session)
1. **CHAT_HANDOFF_TEMPLATE.md** - Start here ALWAYS
2. **QUICK_REFERENCE.md** - For quick lookups
3. **COMPLETE_PROJECT_DOCUMENTATION.md** - As needed for complex changes

### 🐛 For Troubleshooting Issues
1. **QUICK_REFERENCE.md** → Common Issues section
2. **COMPLETE_PROJECT_DOCUMENTATION.md** → Troubleshooting section
3. Specific fix docs (FIXES_SUMMARY.md, etc.) → If issue matches recent fix
4. **This README** → Troubleshooting Guide section below

### 📊 For Understanding Recent Changes
1. **FIXES_SUMMARY.md** - High-level overview
2. **FIXES_APPLIED.md** - Technical details
3. Specific feature docs - For particular features

---

## 🔧 Comprehensive Troubleshooting Guide

### 🚨 Critical Issues & Solutions

#### Issue 1: YTD Data Shows Incorrect Totals
**Symptoms:**
- YTD cumulative stats don't match expected values
- Skins luck totals seem off
- Player totals don't add up

**Root Causes:**
1. **Baseline date mismatch** - Most common
2. **Duplicate data** - Same date processed multiple times
3. **Missing Won_Game values** - NA values in historical data

**Solutions:**
```r
# Check baseline date
baseline_date_file <- "skins_history/baseline_date.txt"
readLines(baseline_date_file)  # Should match ytd_baseline update date

# Check for duplicates
library(dplyr)
all_files <- list.files("skins_history", pattern = "^\\d{4}-\\d{2}-\\d{2}\\.csv$", full.names = TRUE)
all_history <- bind_rows(lapply(all_files, read_csv))
all_history %>% group_by(Date, Player, Team) %>% filter(n() > 1)  # Should be empty

# Check for NA values in Won_Game
all_history %>% filter(is.na(Won_Game)) %>% count()  # Should only be games not yet played
```

**Prevention:**
- Always verify baseline_date.txt matches ytd_baseline.csv update
- Never manually edit historical CSV files
- Let GitHub Actions handle data updates

---

#### Issue 2: Yesterday's Data Shows Wrong Teams
**Symptoms:**
- Yesterday's Results section shows teams that didn't play yesterday
- Matchups are incorrect
- Player assignments don't match actual games

**Root Cause:**
- Scraping from generic URL instead of date-specific URL
- Wrong date calculation for "yesterday"

**Solution:**
```r
# Correct approach (already implemented)
yesterday_ct <- today_ct - days(1)
yesterday_url <- paste0("https://plaintextsports.com/nba/", yesterday_ct, "/")

# WRONG approach (do not use)
# yesterday_url <- "https://plaintextsports.com/nba/"  # This gets "today"
```

**Verification:**
```r
# Check that yesterday_ct is correct
current_time_ct <- now(tzone = "America/Chicago")
current_hour_ct <- hour(current_time_ct)

if (current_hour_ct < 2) {
  skins_date <- as_date(current_time_ct) - days(1)
} else {
  skins_date <- as_date(current_time_ct)
}

yesterday_ct <- skins_date - days(1)
print(paste("Yesterday's date:", yesterday_ct))
```

---

#### Issue 3: Blackout Window Not Working (11 PM - 2 AM)
**Symptoms:**
- System tries to scrape during blackout window
- CSV file not found errors
- Incomplete data displayed

**Root Cause:**
- Time zone calculation error
- Blackout window logic incorrect
- CSV file missing for current date

**Solution:**
```r
# Verify time zone
current_time_ct <- now(tzone = "America/Chicago")
current_hour_ct <- hour(current_time_ct)
cat("Current hour (CT):", current_hour_ct, "\n")

# Verify blackout window logic
is_blackout_window <- current_hour_ct >= 23 | current_hour_ct < 2
cat("Is blackout window?", is_blackout_window, "\n")

# Verify CSV file exists
skins_date <- if (current_hour_ct < 2) {
  as_date(current_time_ct) - days(1)
} else {
  as_date(current_time_ct)
}
file_path <- paste0("skins_history/", skins_date, ".csv")
cat("Looking for:", file_path, "\n")
cat("File exists?", file.exists(file_path), "\n")
```

**Prevention:**
- GitHub Actions should run BEFORE 11 PM CT
- Ensure last daytime run (5 PM CT / 22:00 UTC) completes successfully
- Monitor GitHub Actions logs during evening runs

---

#### Issue 4: Color Coding Not Appearing in Tables
**Symptoms:**
- Player names don't show green/pink backgrounds
- Formatting appears as plain text
- HTML tags visible in output

**Root Cause:**
- `escape = FALSE` missing from kable() call
- `format = "html"` not specified
- cell_spec() parameters incorrect

**Solution:**
```r
# CORRECT approach
Player_Display = case_when(
  !is.na(Won_Skin) & Won_Skin == TRUE ~ 
    cell_spec(Player, background = "#90EE90", color = "#000000 !important", 
              bold = TRUE, format = "html", extra_css = "color: #000000 !important;"),
  !is.na(Won_Skin) & Won_Skin == FALSE ~ 
    cell_spec(Player, background = "#FFB6C6", color = "#000000 !important", 
              bold = TRUE, format = "html", extra_css = "color: #000000 !important;"),
  TRUE ~ Player
)

# In kable call
knitr::kable(
  table_data,
  escape = FALSE,   # Critical!
  format = "html"   # Critical!
)
```

**Verification:**
- View page source to confirm HTML tags are present
- Check browser console for CSS errors
- Verify kableExtra package is loaded

---

#### Issue 5: Team Abbreviations Don't Match
**Symptoms:**
- Teams not matching between draft_data and scraped data
- "WARNING: Teams in scraped data but not in draft_data"
- Missing teams in results

**Root Cause:**
- Inconsistent abbreviations between sources
- New team abbreviation not in standardization map

**Solution:**
```r
# Standardization map (keep updated)
team_replacements <- c(
  "^GS$" = "GSW",      # Golden State
  "^NO$" = "NOP",      # New Orleans
  "^NY$" = "NYK",      # New York Knicks
  "^SA$" = "SAS",      # San Antonio
  "^WSH$" = "WAS"      # Washington
)

# Apply to scraped data
scraped_data <- scraped_data %>%
  mutate(
    Team1 = str_replace_all(Team1, team_replacements),
    Team2 = str_replace_all(Team2, team_replacements)
  )
```

**When Adding New Team Mappings:**
1. Check plaintextsports.com abbreviation
2. Check sportsline.com abbreviation
3. Add to team_replacements if different
4. Update in ALL chunks that standardize teams

---

#### Issue 6: Zero-Sum Matchups Not Detecting Correctly
**Symptoms:**
- Zero-sum matchups table empty when it shouldn't be
- Incorrectly identifying matchups as zero-sum
- Max Skins calculation wrong

**Root Cause:**
- game_id not matching between teams
- Pick comparison logic incorrect
- Same player check failing

**Solution:**
```r
# Correct zero-sum detection
zero_sum_games <- todays_picks %>%
  group_by(game_id) %>%
  filter(
    n() == 2,  # Exactly 2 teams in the game
    (all(Pick == "W") | all(Pick == "L"))  # Both W or both L
  )

# Self zero-sum (same player)
self_zero_sum <- todays_picks %>%
  group_by(game_id) %>%
  filter(n() == 2) %>%
  summarise(
    is_self_zero_sum = length(unique(Player)) == 1 & length(unique(Pick)) == 1
  )
```

**Verification:**
```r
# Manual check
todays_picks %>%
  group_by(game_id) %>%
  summarise(
    players = paste(unique(Player), collapse = ", "),
    picks = paste(unique(Pick), collapse = ", "),
    is_zero_sum = n() == 2 & (all(Pick == "W") | all(Pick == "L"))
  )
```

---

### ⚠️ Common Warnings & What They Mean

#### Warning: "In blackout window, but file not found"
**Meaning:** System is in 11 PM - 2 AM window but can't find today's CSV
**Usually Caused By:** 
- GitHub Actions didn't run successfully earlier
- File path incorrect
- Date calculation wrong
**Action:** Check GitHub Actions logs for earlier run failures

#### Warning: "Teams in scraped data but not in draft_data"
**Meaning:** Sportsline.com has a team that doesn't match any in draft_data
**Usually Caused By:**
- New team name format
- Abbreviation changed
- Team renamed
**Action:** Add team to draft_data tribble or to team_replacements map

#### Warning: "Row contains NA values"
**Meaning:** Some expected values are missing from scraped data
**Usually Caused By:**
- Game postponed
- Odds not yet posted
- Scraping error
**Action:** Usually safe to ignore if only a few rows; investigate if widespread

---

### 🎯 Debugging Tips & Techniques

#### Tip 1: Enable Verbose Output
```r
# Add to chunk options
#| message: true
#| warning: true

# Add diagnostic prints
cat("Current time (CT):", as.character(current_time_ct), "\n")
cat("Skins date:", as.character(skins_date), "\n")
cat("Blackout window?", is_blackout_window, "\n")
cat("Number of games scraped:", nrow(todays_picks), "\n")
```

#### Tip 2: Check Data Flow at Each Step
```r
# After scraping
print(paste("Games scraped:", nrow(game_data)))

# After filtering
print(paste("Games after filter:", nrow(todays_picks)))

# After join
print(paste("Games after join:", nrow(todays_picks)))

# Check for NAs
print(paste("NA Expected Skins:", sum(is.na(todays_picks$`Expected Skins`))))
```

#### Tip 3: Validate Historical Data
```r
# Check date range
all_files <- list.files("skins_history", pattern = "^\\d{4}-\\d{2}-\\d{2}\\.csv$")
dates <- as_date(str_extract(all_files, "\\d{4}-\\d{2}-\\d{2}"))
print(paste("Date range:", min(dates), "to", max(dates)))

# Check for gaps
date_seq <- seq(min(dates), max(dates), by = "day")
missing_dates <- setdiff(date_seq, dates)
if (length(missing_dates) > 0) {
  print("Missing dates:")
  print(missing_dates)
}

# Check row counts
for (file in all_files) {
  data <- read_csv(file.path("skins_history", file), show_col_types = FALSE)
  cat(file, ":", nrow(data), "rows\n")
}
```

#### Tip 4: Test Color Coding Logic Separately
```r
# Create test data
test_data <- data.frame(
  Player = c("Alice", "Bob", "Charlie"),
  Won_Skin = c(TRUE, FALSE, NA)
)

# Apply formatting
test_data <- test_data %>%
  mutate(
    Player_Display = case_when(
      !is.na(Won_Skin) & Won_Skin == TRUE ~ 
        cell_spec(Player, background = "#90EE90", format = "html"),
      !is.na(Won_Skin) & Won_Skin == FALSE ~ 
        cell_spec(Player, background = "#FFB6C6", format = "html"),
      TRUE ~ Player
    )
  )

# Display
knitr::kable(test_data, escape = FALSE, format = "html")
```

---

## 🔍 Understanding System Architecture

### Data Flow Diagram

```
[Sportsline.com] → [Web Scraper] → [todays_picks]
                                          ↓
                                    [Calculate Expected Skins]
                                          ↓
                                    [Display Tables]
                                          ↓
[Plaintextsports.com] → [Results Scraper] → [Won_Game Data]
                                          ↓
                                    [Join with todays_picks]
                                          ↓
                                    [todays_results]
                                          ↓
                                    [Save to CSV] → [skins_history/YYYY-MM-DD.csv]
                                          ↓
                                    [Display Results & Color Coding]
```

### Time Zone & Date Logic

```
Current Time (CT)  →  Skins Date Calculation
------------------     ----------------------
12:00 AM - 1:59 AM  →  Previous Calendar Day
2:00 AM - 11:59 PM  →  Current Calendar Day
```

**Why?** Games often end after midnight, so we wait until 2 AM to "roll over" to the next skins day.

### Blackout Window Logic

```
Evening (11 PM) → Scrape one last time → Save CSV
                          ↓
                   [11 PM - 2 AM]
                          ↓
                   Load from CSV only
                          ↓
Morning (2 AM)  → Resume live scraping
```

**Why?** Between 11 PM and 2 AM, odds sites may be inconsistent. We rely on the last good scrape saved to CSV.

---

## 📊 File Organization Best Practices

### skins_history/ Directory Structure
```
skins_history/
├── 2025-10-24.csv      # Daily game data
├── 2025-10-25.csv
├── 2025-10-26.csv
├── ...
├── 2025-11-01.csv
├── ytd_baseline.csv    # Baseline cumulative stats
└── baseline_date.txt   # Date baseline was updated
```

### CSV File Format
```csv
Date,Player,Team,Abbr,Pick,Expected_Skins,Won_Game,Actual_Skins,Skins_Luck
2025-11-01,Adam,Boston Celtics,BOS,W,0.33059252352292956,NA,NA,NA
```

**Key Columns:**
- `Date`: YYYY-MM-DD format
- `Player`: Player name (Adam, Brian, Eristeo, Kenneth, Matt, Thomas)
- `Team`: Full team name
- `Abbr`: 2-3 letter abbreviation (must match draft_data)
- `Pick`: W or L
- `Expected_Skins`: Decimal 0-1
- `Won_Game`: TRUE/FALSE/NA
- `Actual_Skins`: 0, 1, or NA
- `Skins_Luck`: Actual - Expected

---

## 🚀 GitHub Actions Configuration

### Workflow Schedule Explanation

```yaml
# Daytime runs (every 4 hours)
- cron: '0 14 * * *'  #  9:00 AM CDT (14:00 UTC)
- cron: '0 18 * * *'  #  1:00 PM CDT (18:00 UTC)
- cron: '0 22 * * *'  #  5:00 PM CDT (22:00 UTC)

# Evening runs (every 30 mins)
- cron: '0 0 * * *'   #  7:00 PM CDT (00:00 UTC next day)
- cron: '30 0 * * *'  #  7:30 PM CDT
- cron: '0 1 * * *'   #  8:00 PM CDT
# ... continues until 1:00 AM CDT
```

**Strategy:**
- Daytime: Updates every 4 hours (low frequency when few games)
- Evening: Updates every 30 mins (high frequency during prime game time)
- Last run: 10:30 PM CDT (saves CSV before blackout window)

### Common GitHub Actions Issues

#### Issue: Workflow Not Running
**Symptoms:** No recent runs in Actions tab
**Causes:**
1. Workflow file syntax error
2. Repository not set to allow Actions
3. Quota exceeded (rare)

**Solution:**
1. Check workflow file validity: https://www.yamllint.com/
2. Settings → Actions → Allow all actions
3. Check Actions usage limits

#### Issue: Workflow Fails During Render
**Symptoms:** Red X on workflow run, error in logs
**Common Causes:**
1. R package installation failed
2. Scraping returned empty data
3. Quarto render error
4. Network issue

**Solution:**
```bash
# Check logs for specific error
# Look for lines starting with "Error in..." or "Warning:"

# Common fixes:
# 1. Add missing R package to install step
# 2. Add error handling to scraping code
# 3. Update Quarto version
# 4. Add retry logic for network calls
```

#### Issue: Git Push Fails
**Symptoms:** Workflow completes but changes not committed
**Causes:**
1. No changes to commit
2. Git credentials issue
3. Protected branch

**Solution:**
```yaml
# Add continue-on-error to prevent failure
- name: Commit history updates
  run: |
    git add skins_history/*.csv
    git diff --staged --quiet || git commit -m "Update skins history"
    git push
  continue-on-error: true
```

---

## 💡 Advanced Tips & Tricks

### Tip 1: Testing Locally Before Deployment
```bash
# Test Quarto render locally
cd /path/to/project
quarto render skins_today.qmd --to html

# Check output
open _site/index.html  # Mac
xdg-open _site/index.html  # Linux
start _site/index.html  # Windows
```

### Tip 2: Simulating Different Times
```r
# Override current time for testing
test_time <- as.POSIXct("2025-11-01 23:30:00", tz = "America/Chicago")
current_hour_ct <- hour(test_time)
# Now test blackout window logic
```

### Tip 3: Bulk Updating Historical Data
```r
# If you need to recalculate all historical files
all_files <- list.files("skins_history", pattern = "^\\d{4}-\\d{2}-\\d{2}\\.csv$", full.names = TRUE)

for (file in all_files) {
  data <- read_csv(file, show_col_types = FALSE)
  
  # Make corrections
  data <- data %>%
    mutate(
      # Your corrections here
      Skins_Luck = Actual_Skins - Expected_Skins
    )
  
  # Save back
  write_csv(data, file)
}
```

### Tip 4: Monitoring System Health
```r
# Create health check function
check_system_health <- function() {
  health_report <- list()
  
  # Check 1: Recent files
  recent_files <- list.files("skins_history", pattern = "^\\d{4}-\\d{2}-\\d{2}\\.csv$")
  recent_dates <- as_date(str_extract(recent_files, "\\d{4}-\\d{2}-\\d{2}"))
  days_since_last <- as.numeric(Sys.Date() - max(recent_dates))
  health_report$days_since_last_file <- days_since_last
  health_report$files_healthy <- days_since_last <= 2
  
  # Check 2: Baseline date
  baseline_date <- as_date(readLines("skins_history/baseline_date.txt")[1])
  health_report$baseline_date <- baseline_date
  health_report$baseline_current <- baseline_date >= (Sys.Date() - days(7))
  
  # Check 3: YTD data completeness
  ytd_baseline <- read_csv("skins_history/ytd_baseline.csv", show_col_types = FALSE)
  health_report$all_players_in_baseline <- nrow(ytd_baseline) == 6
  
  return(health_report)
}

# Run check
health <- check_system_health()
print(health)
```

---

## 🎓 Understanding Edge Cases

### Edge Case 1: Same Player, Both Teams in Same Game
**Scenario:** Adam has both LAL (W) and BOS (L) in the same game

**Behavior:**
- Both teams appear in todays_picks
- Expected skins calculated for each independently
- At most one can win → zero-sum for that player
- Max Skins reduced by 1 for this player

**Code Handling:**
```r
self_zero_sum <- todays_picks %>%
  group_by(game_id) %>%
  filter(n() == 2) %>%
  summarise(
    is_self_zero_sum = length(unique(Player)) == 1 & length(unique(Pick)) == 1
  )
```

### Edge Case 2: Game Postponed/Cancelled
**Scenario:** Game scheduled but postponed before it starts

**Behavior:**
- Team appears in todays_picks (from morning scrape)
- Never gets Won_Game value
- Remains NA in results
- Does not contribute to YTD totals

**Prevention:** System correctly handles NA values, no action needed

### Edge Case 3: Overtime Game
**Scenario:** Game goes to OT, final score different from end of regulation

**Behavior:**
- Plaintextsports.com shows final score including OT
- Won_Game based on final result (correct)
- No special handling needed

### Edge Case 4: Doubleheader (Rare)
**Scenario:** Same teams play twice in one day

**Behavior:**
- Both games scraped separately
- game_id differentiates them
- Both contribute to daily totals

**Note:** NBA rarely has doubleheaders, but system handles them correctly

### Edge Case 5: Date Line Issues
**Scenario:** Game starts before midnight, ends after midnight

**Behavior:**
- Assigned to date based on scheduled start time
- 2 AM rollover ensures game is complete before date change
- Historical scraping uses date-specific URL, gets correct game

---

## 📚 Code Pattern Reference

### Pattern 1: Safe Data Joining
```r
# GOOD: Use left_join with by parameter
result <- data1 %>%
  left_join(data2, by = c("Team" = "Abbr"))

# BAD: Implicit join (can cause unexpected matches)
result <- data1 %>%
  left_join(data2)
```

### Pattern 2: Handling NA Values in Calculations
```r
# GOOD: Explicitly handle NA
value <- case_when(
  is.na(x) ~ NA_real_,
  x > 0 ~ 1,
  TRUE ~ 0
)

# BAD: NA propagates unexpectedly
value <- if_else(x > 0, 1, 0)  # Returns NA if x is NA
```

### Pattern 3: Date Filtering
```r
# GOOD: Filter on date column explicitly
data %>%
  filter(game_date_ct == target_date)

# BAD: Filter on derived values
data %>%
  filter(as_date(game_time_ct) == target_date)  # Slower, less clear
```

### Pattern 4: Grouped Calculations
```r
# GOOD: Use group_by with summarise
result <- data %>%
  group_by(game_id) %>%
  summarise(
    player1 = first(Player),
    player2 = if (n() > 1) nth(Player, 2) else NA_character_,
    .groups = 'drop'  # Always drop groups after summarise
  )

# BAD: Forget to ungroup
result <- data %>%
  group_by(game_id) %>%
  summarise(...)
  # Still grouped! Can cause issues downstream
```

### Pattern 5: Color Coding HTML
```r
# GOOD: Complete cell_spec with all parameters
Player_Display = cell_spec(
  Player, 
  background = "#90EE90", 
  color = "#000000 !important",
  bold = TRUE, 
  format = "html",
  extra_css = "color: #000000 !important;"
)

# BAD: Missing format parameter
Player_Display = cell_spec(Player, background = "#90EE90")  # Won't work
```

---

## 🎯 Quick Command Reference

### R/Quarto Commands
```r
# Render document locally
quarto render skins_today.qmd --to html

# Check for syntax errors
quarto check

# Install missing packages
install.packages(c("rvest", "httr", "dplyr", "tidyr", "stringr", 
                   "lubridate", "tibble", "knitr", "kableExtra", 
                   "readr", "ggplot2"))

# Load all packages
if (!require("pacman")) install.packages("pacman")
pacman::p_load(rvest, httr, dplyr, tidyr, stringr, lubridate, 
               tibble, knitr, kableExtra, readr, ggplot2)
```

### Git Commands
```bash
# Check status
git status

# Add changes
git add skins_history/*.csv

# Commit
git commit -m "Update skins history - YYYY-MM-DD"

# Push
git push origin main

# View recent commits
git log --oneline -10

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

### File Management
```bash
# List history files
ls -lh skins_history/

# Check file size
du -sh skins_history/

# Count CSV files
ls skins_history/*.csv | wc -l

# View last 10 lines of CSV
tail -10 skins_history/2025-11-01.csv

# Search for specific player
grep "Adam" skins_history/*.csv
```

---

## 📊 Project Statistics

### Documentation Coverage
- **Total Documentation Files:** 20+ files
- **Total Documentation Lines:** ~3,500+ lines
- **Core Documentation:** ~1,000 lines (3 essential files)
- **Average Doc File Size:** ~150 lines
- **Most Comprehensive:** COMPLETE_PROJECT_DOCUMENTATION.md (400+ lines)
- **Most Referenced:** CHAT_HANDOFF_TEMPLATE.md

### Code Statistics
- **Main Code File:** skins_today.qmd
- **Total Lines:** ~1,200 lines
- **R Code Chunks:** 15+ chunks
- **Functions Defined:** 5+ helper functions
- **Data Sources:** 2 external websites
- **Tables Generated:** 10+ tables
- **Charts Generated:** 2 charts

### Historical Data
- **Start Date:** October 24, 2025
- **Total Days Tracked:** 8+ days
- **Games per Day:** ~5-12 games
- **Players Tracked:** 6 players
- **Teams Tracked:** 30 NBA teams

---

## 🔐 Security & Privacy Notes

### Data Sources
- **Sportsline.com:** Public betting odds (no authentication required)
- **Plaintextsports.com:** Public game scores (no authentication required)

### No Sensitive Data
- No personal information stored
- No betting transactions
- No financial data
- Only publicly available sports data

### GitHub Pages
- Static site (no server-side code)
- No user authentication
- No data collection
- Public access

---

## 🚀 Future Enhancement Ideas

### Potential Features
1. **Historical comparison charts** - Compare current season to past seasons
2. **Player vs player head-to-head** - Track matchups between specific players
3. **Streak tracking** - Longest winning/losing streaks
4. **Best/worst picks** - Teams that consistently over/underperform
5. **Email notifications** - Daily summary emails
6. **Mobile optimization** - Better mobile layouts
7. **Interactive charts** - Plotly instead of ggplot2
8. **API endpoint** - Programmatic access to data
9. **Export functionality** - Download data as Excel
10. **Live updates** - WebSocket for real-time score updates

### Known Limitations
1. **Historical data limited** - Only goes back to Oct 24, 2025
2. **No automated alerts** - Must check page manually
3. **Single sport** - Only NBA (could expand)
4. **Basic visualizations** - Could add more chart types
5. **No user accounts** - Everyone sees same data

---

## 🎯 Success Checklist

### Daily Operation Verification
- [ ] GitHub Actions ran successfully (check Actions tab)
- [ ] New CSV file created in skins_history/
- [ ] Today's games visible on page
- [ ] Results populated for completed games
- [ ] Color coding working on all tables
- [ ] Yesterday's section shows correct date
- [ ] YTD totals look reasonable
- [ ] Charts displaying correctly
- [ ] No error messages visible

### Weekly Maintenance
- [ ] Review GitHub Actions logs for warnings
- [ ] Check skins_history/ directory size
- [ ] Verify no duplicate data
- [ ] Spot-check historical accuracy
- [ ] Review player totals for anomalies
- [ ] Test page on different browsers
- [ ] Check mobile display

### Monthly Tasks
- [ ] Update ytd_baseline.csv (if needed)
- [ ] Review and clean up old branches
- [ ] Check for package updates
- [ ] Review documentation accuracy
- [ ] Archive old documentation
- [ ] Performance optimization review

---

## 📞 Getting Help

### When Things Break
1. **Check this README** → Troubleshooting section
2. **Check QUICK_REFERENCE.md** → Common issues
3. **Check COMPLETE_PROJECT_DOCUMENTATION.md** → Detailed troubleshooting
4. **Check specific fix docs** → Recent issues
5. **Start new Claude chat** → Use CHAT_HANDOFF_TEMPLATE.md

### Information Hierarchy
```
Quick Answer → QUICK_REFERENCE.md
↓
Detailed Info → COMPLETE_PROJECT_DOCUMENTATION.md
↓
Recent Changes → FIXES_SUMMARY.md / FIXES_APPLIED.md
↓
Specific Issue → Individual fix docs
↓
New Chat → CHAT_HANDOFF_TEMPLATE.md
```

---

## 📝 Document Change Log

### November 1, 2025
- Created enhanced README with comprehensive troubleshooting
- Added extensive edge case documentation
- Included code pattern reference
- Added system health monitoring tips
- Expanded GitHub Actions documentation
- Added security & privacy notes

### October 31, 2025
- Original README created
- Basic documentation index
- File organization guide

---

## 💾 Backup Recommendations

### Essential Files to Backup
1. **skins_history/** - All CSV files (most critical)
2. **CHAT_HANDOFF_TEMPLATE.md** - For continuity
3. **QUICK_REFERENCE.md** - For quick reference
4. **COMPLETE_PROJECT_DOCUMENTATION.md** - Complete info
5. **skins_today.qmd** - Source code

### Backup Strategy
```bash
# Create backup
tar -czf nba-skins-backup-$(date +%Y%m%d).tar.gz \
  skins_history/ \
  *.md \
  skins_today.qmd \
  .github/workflows/

# Restore from backup
tar -xzf nba-skins-backup-YYYYMMDD.tar.gz
```

### Cloud Backup Options
- GitHub repository (already backed up)
- Google Drive / Dropbox (manual backup)
- AWS S3 / Azure Blob (for automation)

---

## 🎓 Learning Resources

### R & Quarto
- [Quarto Documentation](https://quarto.org/docs/guide/)
- [R for Data Science](https://r4ds.hadley.nz/)
- [ggplot2 Documentation](https://ggplot2.tidyverse.org/)

### Web Scraping
- [rvest Documentation](https://rvest.tidyverse.org/)
- [SelectorGadget](https://selectorgadget.com/) - For finding CSS selectors

### GitHub Actions
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions for R](https://github.com/r-lib/actions)

---

## ✅ Final Notes

This project is **fully functional and production-ready** as of November 1, 2025. All documentation is current and accurate. The system runs automatically via GitHub Actions and requires minimal maintenance.

### Key Success Factors
1. ✅ Comprehensive documentation
2. ✅ Automated deployment
3. ✅ Robust error handling
4. ✅ Historical data preservation
5. ✅ Clear troubleshooting guides
6. ✅ Active maintenance strategy

### Project Status: STABLE & PRODUCTION

**Last Updated:** November 1, 2025  
**Version:** 2.0  
**Status:** Production-ready with comprehensive documentation

---

**Remember:** When in doubt, start with CHAT_HANDOFF_TEMPLATE.md for new sessions, use QUICK_REFERENCE.md for quick lookups, and dive into COMPLETE_PROJECT_DOCUMENTATION.md for deep understanding. This README ties it all together!
