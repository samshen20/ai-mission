# Test Cases: GitHub Login Functionality

## Overview
- **Feature**: GitHub Login / Authentication
- **Requirements Source**: GitHub login page (github.com/login) — standard username/password, OAuth, 2FA, and SSO flows
- **Test Coverage**: Functional login flows, edge cases, error handling, state transitions, and security scenarios
- **Last Updated**: 2026-06-16

---

## Test Case Categories

### 1. Functional Tests

#### TC-F-001: Successful Login with Valid Username and Password
- **Requirement**: User can log in using a registered username/email and correct password
- **Priority**: High
- **Preconditions**:
  - User has a registered GitHub account
  - User is on the GitHub login page (`github.com/login`)
  - 2FA is not enabled on the account
- **Test Steps**:
  ```gherkin
  Feature: GitHub Login

    Scenario: Successful login with valid credentials
      Given I am on the GitHub login page
      When I enter a valid registered username or email in the "Username or email address" field
      And I enter the correct password in the "Password" field
      And I click the "Sign in" button
      Then I should be redirected to the GitHub dashboard
      And I should see my profile avatar in the top-right navigation
      And I should be authenticated as the correct user
  ```
- **Postconditions**: User session is established; user is on the GitHub dashboard

---

#### TC-F-002: Successful Login with Valid Email Address
- **Requirement**: User can log in using their registered email instead of username
- **Priority**: High
- **Preconditions**:
  - User has a registered GitHub account with a verified email
  - User is on the GitHub login page
- **Test Steps**:
  ```gherkin
  Scenario: Successful login using email address
    Given I am on the GitHub login page
    When I enter a valid registered email address in the "Username or email address" field
    And I enter the correct password in the "Password" field
    And I click the "Sign in" button
    Then I should be redirected to the GitHub dashboard
    And I should be authenticated as the correct user
  ```
- **Postconditions**: User session is established; user is on the GitHub dashboard

---

#### TC-F-003: Successful Login with Two-Factor Authentication (TOTP)
- **Requirement**: User with 2FA enabled can log in by providing a valid TOTP code
- **Priority**: High
- **Preconditions**:
  - User has a registered account with 2FA (TOTP app) enabled
  - User has access to their authenticator app
- **Test Steps**:
  ```gherkin
  Scenario: Successful login with TOTP two-factor authentication
    Given I am on the GitHub login page
    And my account has 2FA enabled with a TOTP authenticator app
    When I enter my valid username and password
    And I click "Sign in"
    Then I should be redirected to the 2FA verification page
    When I enter the current 6-digit TOTP code from my authenticator app
    And I click "Verify"
    Then I should be redirected to the GitHub dashboard
    And I should be authenticated as the correct user
  ```
- **Postconditions**: User session is established with 2FA verified

---

#### TC-F-004: Successful Login Using SMS Two-Factor Authentication
- **Requirement**: User with SMS-based 2FA can log in by providing the code sent via SMS
- **Priority**: Medium
- **Preconditions**:
  - User has SMS-based 2FA enabled on their account
  - User has access to the registered phone number
- **Test Steps**:
  ```gherkin
  Scenario: Successful login with SMS two-factor authentication
    Given I am on the GitHub login page
    And my account has SMS-based 2FA enabled
    When I enter my valid username and password and click "Sign in"
    Then I should be redirected to the 2FA verification page
    When I receive an SMS with a verification code
    And I enter the SMS code in the verification field
    And I click "Verify"
    Then I should be redirected to the GitHub dashboard
  ```
- **Postconditions**: User session is established

---

#### TC-F-005: Successful Login with Recovery Code
- **Requirement**: User can log in using a 2FA recovery code if authenticator is unavailable
- **Priority**: Medium
- **Preconditions**:
  - User has 2FA enabled on their account
  - User has unused recovery codes
- **Test Steps**:
  ```gherkin
  Scenario: Login using a 2FA recovery code
    Given I am on the GitHub login page
    And my account has 2FA enabled
    When I enter valid credentials and click "Sign in"
    Then I am on the 2FA verification page
    When I click "Use a recovery code or begin 2FA account recovery"
    And I enter a valid unused recovery code
    And I click "Verify"
    Then I should be redirected to the GitHub dashboard
    And the used recovery code should be invalidated
  ```
- **Postconditions**: User is logged in; recovery code is consumed

---

#### TC-F-006: Successful Login via OAuth (Sign in with Google/Organization SSO)
- **Requirement**: Enterprise users or users with OAuth configured can sign in via SSO
- **Priority**: Medium
- **Preconditions**:
  - User's organization has configured SAML SSO on GitHub
  - User has a valid organizational identity provider (IdP) account
- **Test Steps**:
  ```gherkin
  Scenario: Login via SAML SSO for an organization
    Given I am on the GitHub login page
    When I enter my organization's SSO email and click "Sign in"
    Then I should be redirected to my organization's SSO identity provider page
    When I complete authentication on the IdP
    Then I should be redirected back to GitHub
    And I should be authenticated as the correct user
    And I should have access to organization resources
  ```
- **Postconditions**: User is logged in with organizational access

---

#### TC-F-007: "Remember Me" / Stay Signed In
- **Requirement**: User can remain logged in across browser sessions
- **Priority**: Low
- **Preconditions**:
  - User is on the GitHub login page
  - Browser supports persistent cookies
- **Test Steps**:
  ```gherkin
  Scenario: User stays signed in after browser restart
    Given I am on the GitHub login page
    When I enter valid credentials and click "Sign in"
    And a persistent session cookie is set
    And I close and reopen the browser
    And I navigate to github.com
    Then I should still be logged in without re-entering credentials
  ```
- **Postconditions**: User session persists across browser restarts

---

### 2. Edge Case Tests

#### TC-E-001: Username Field with Maximum Length Input
- **Requirement**: Login form handles usernames at maximum allowed length (39 characters)
- **Priority**: Low
- **Preconditions**:
  - User has an account with a 39-character username
- **Test Steps**:
  ```gherkin
  Scenario: Login with a username at maximum allowed length (39 chars)
    Given I am on the GitHub login page
    When I enter a 39-character valid username in the username field
    And I enter the correct password
    And I click "Sign in"
    Then I should be successfully authenticated
    And I should be redirected to the dashboard
  ```
- **Postconditions**: User is logged in successfully

---

#### TC-E-002: Username with Mixed Case (Case Insensitivity)
- **Requirement**: GitHub usernames are case-insensitive during login
- **Priority**: Medium
- **Preconditions**:
  - User has an account with username "octocat"
- **Test Steps**:
  ```gherkin
  Scenario: Login with username in different casing
    Given I am on the GitHub login page
    And my GitHub username is "octocat"
    When I enter "OCTOCAT" in the username field
    And I enter the correct password
    And I click "Sign in"
    Then I should be successfully authenticated as "octocat"
  ```
- **Postconditions**: User is logged in

---

#### TC-E-003: Email with Leading and Trailing Whitespace
- **Requirement**: Login form trims whitespace from the email/username field
- **Priority**: Low
- **Preconditions**:
  - User has a valid account
- **Test Steps**:
  ```gherkin
  Scenario: Login with leading/trailing whitespace in the email field
    Given I am on the GitHub login page
    When I enter "  user@example.com  " (with spaces) in the email field
    And I enter the correct password
    And I click "Sign in"
    Then the whitespace should be trimmed automatically
    And I should be successfully authenticated
  ```
- **Postconditions**: User is logged in

---

#### TC-E-004: Password with Special Characters
- **Requirement**: Passwords containing special characters are accepted
- **Priority**: Medium
- **Preconditions**:
  - User account has a password containing special characters (e.g., `P@$$w0rd!#%^&*`)
- **Test Steps**:
  ```gherkin
  Scenario: Successful login with a password containing special characters
    Given I am on the GitHub login page
    When I enter a valid username
    And I enter a password containing special characters "P@$$w0rd!#%^&*"
    And I click "Sign in"
    Then I should be successfully authenticated
  ```
- **Postconditions**: User is logged in

---

#### TC-E-005: TOTP Code Entry at Boundary (Code About to Expire)
- **Requirement**: A TOTP code entered within its validity window should be accepted
- **Priority**: Medium
- **Preconditions**:
  - User has TOTP 2FA enabled
  - A new TOTP code was generated less than 30 seconds ago
- **Test Steps**:
  ```gherkin
  Scenario: TOTP code entered at the last second of validity
    Given I am on the 2FA verification page
    And the current TOTP code has 1 second remaining before expiry
    When I enter the current TOTP code
    And I click "Verify" within the validity window
    Then I should be successfully authenticated
  ```
- **Postconditions**: User is logged in

---

### 3. Error Handling Tests

#### TC-ERR-001: Login with Incorrect Password
- **Requirement**: System displays an error for an incorrect password
- **Priority**: High
- **Preconditions**:
  - User has a registered GitHub account
- **Test Steps**:
  ```gherkin
  Scenario: Login attempt with incorrect password
    Given I am on the GitHub login page
    When I enter a valid registered username
    And I enter an incorrect password
    And I click "Sign in"
    Then I should remain on the login page
    And I should see the error message "Incorrect username or password."
    And I should not be authenticated
  ```
- **Postconditions**: User session is not created; login page is shown with error

---

#### TC-ERR-002: Login with Non-Existent Username
- **Requirement**: System displays an error for an unrecognised username
- **Priority**: High
- **Preconditions**:
  - User is on the GitHub login page
- **Test Steps**:
  ```gherkin
  Scenario: Login attempt with a non-existent username
    Given I am on the GitHub login page
    When I enter a username that does not exist on GitHub
    And I enter any password
    And I click "Sign in"
    Then I should remain on the login page
    And I should see the error message "Incorrect username or password."
    And I should not be authenticated
  ```
- **Postconditions**: User session is not created (error message is identical to wrong password to prevent username enumeration)

---

#### TC-ERR-003: Login with Empty Username Field
- **Requirement**: System validates that the username field is not empty
- **Priority**: High
- **Preconditions**:
  - User is on the GitHub login page
- **Test Steps**:
  ```gherkin
  Scenario: Login attempt with empty username field
    Given I am on the GitHub login page
    When I leave the "Username or email address" field empty
    And I enter a password
    And I click "Sign in"
    Then I should see a validation error indicating the username field is required
    And I should not be authenticated
  ```
- **Postconditions**: User remains on the login page

---

#### TC-ERR-004: Login with Empty Password Field
- **Requirement**: System validates that the password field is not empty
- **Priority**: High
- **Preconditions**:
  - User is on the GitHub login page
- **Test Steps**:
  ```gherkin
  Scenario: Login attempt with empty password field
    Given I am on the GitHub login page
    When I enter a valid username
    And I leave the "Password" field empty
    And I click "Sign in"
    Then I should see a validation error indicating the password field is required
    And I should not be authenticated
  ```
- **Postconditions**: User remains on the login page

---

#### TC-ERR-005: Login with Both Fields Empty
- **Requirement**: System validates both required fields before submission
- **Priority**: Medium
- **Preconditions**:
  - User is on the GitHub login page
- **Test Steps**:
  ```gherkin
  Scenario: Login attempt with all fields empty
    Given I am on the GitHub login page
    When I leave both the username and password fields empty
    And I click "Sign in"
    Then I should see validation errors for both required fields
    And I should not be authenticated
  ```
- **Postconditions**: User remains on the login page

---

#### TC-ERR-006: Account Locked After Multiple Failed Login Attempts (Rate Limiting)
- **Requirement**: System throttles or temporarily locks the account after repeated failed logins
- **Priority**: High
- **Preconditions**:
  - User has a registered account
  - User attempts login with incorrect credentials multiple times (threshold: typically 5–10 attempts)
- **Test Steps**:
  ```gherkin
  Scenario: Account temporarily locked after repeated failed login attempts
    Given I am on the GitHub login page
    When I enter a valid username
    And I enter an incorrect password 10 consecutive times
    Then I should see a message indicating the account is temporarily locked or CAPTCHA is triggered
    And I should not be able to log in immediately even with the correct password
    And I may be prompted to verify via email or complete a CAPTCHA challenge
  ```
- **Postconditions**: Account login is rate-limited; user must wait or verify identity

---

#### TC-ERR-007: Invalid TOTP Code Entered
- **Requirement**: System rejects an expired or incorrect TOTP code
- **Priority**: High
- **Preconditions**:
  - User has TOTP 2FA enabled and has passed the password check
- **Test Steps**:
  ```gherkin
  Scenario: Invalid TOTP code entered during 2FA
    Given I am on the 2FA verification page
    When I enter an incorrect or expired 6-digit TOTP code
    And I click "Verify"
    Then I should see the error message "Invalid two-factor code."
    And I should remain on the 2FA verification page
    And I should not be authenticated
  ```
- **Postconditions**: User is not logged in; 2FA page is shown with error

---

#### TC-ERR-008: Already-Used Recovery Code Rejected
- **Requirement**: A previously used 2FA recovery code cannot be reused
- **Priority**: Medium
- **Preconditions**:
  - User has 2FA enabled and a recovery code has already been used
- **Test Steps**:
  ```gherkin
  Scenario: Attempt to reuse an already-consumed recovery code
    Given I am on the 2FA recovery code input page
    When I enter a recovery code that has already been used
    And I click "Verify"
    Then I should see an error indicating the code is invalid or already used
    And I should not be authenticated
  ```
- **Postconditions**: User is not logged in

---

#### TC-ERR-009: Login Page Accessed via Non-HTTPS (Security)
- **Requirement**: The login page must only be served over HTTPS
- **Priority**: High
- **Preconditions**:
  - User attempts to access `http://github.com/login` (non-secure)
- **Test Steps**:
  ```gherkin
  Scenario: Access login page over HTTP is redirected to HTTPS
    Given I navigate to "http://github.com/login"
    Then I should be automatically redirected to "https://github.com/login"
    And the connection should use TLS encryption
    And no credentials should be transmitted over plain HTTP
  ```
- **Postconditions**: User is on the secure HTTPS login page

---

#### TC-ERR-010: Session Expired — Re-authentication Required
- **Requirement**: User is prompted to log in again when their session has expired
- **Priority**: Medium
- **Preconditions**:
  - User was previously logged in but the session has since expired
- **Test Steps**:
  ```gherkin
  Scenario: Accessing GitHub after session expiry
    Given I was previously logged into GitHub
    And my session has expired (e.g., after timeout or cookie deletion)
    When I navigate to "https://github.com"
    Then I should be redirected to the login page
    And I should see a message or indicator that I need to sign in again
  ```
- **Postconditions**: User must re-authenticate

---

### 4. State Transition Tests

#### TC-ST-001: Logout and Subsequent Login
- **Requirement**: User can log out and then log back in successfully
- **Priority**: High
- **Preconditions**:
  - User is currently logged in to GitHub
- **Test Steps**:
  ```gherkin
  Scenario: Log out and log back in
    Given I am logged in to GitHub
    When I click my profile avatar in the top-right corner
    And I click "Sign out"
    Then I should be redirected to the GitHub homepage
    And I should see the "Sign in" button in the navigation
    And my session cookie should be invalidated
    When I navigate to "https://github.com/login"
    And I enter valid credentials and click "Sign in"
    Then I should be successfully logged back in
  ```
- **Postconditions**: A new authenticated session is created

---

#### TC-ST-002: Password Changed — Previous Session Invalidated
- **Requirement**: Changing the account password invalidates all existing sessions
- **Priority**: High
- **Preconditions**:
  - User is logged in on two separate browser sessions
- **Test Steps**:
  ```gherkin
  Scenario: Password change invalidates existing sessions
    Given I am logged in on Browser A and Browser B simultaneously
    When I change my account password on Browser A
    Then my session on Browser A should remain valid (or be re-authenticated)
    And my session on Browser B should be invalidated
    When I attempt to perform an action on Browser B
    Then I should be redirected to the login page on Browser B
  ```
- **Postconditions**: All sessions except the one that changed the password are terminated

---

#### TC-ST-003: Enabling 2FA Mid-Session
- **Requirement**: Enabling 2FA on an active session takes effect on the next login
- **Priority**: Medium
- **Preconditions**:
  - User is logged in without 2FA enabled
- **Test Steps**:
  ```gherkin
  Scenario: Enable 2FA and verify it is required on next login
    Given I am logged in to GitHub without 2FA enabled
    When I navigate to account security settings
    And I enable two-factor authentication using a TOTP app
    And I save and confirm the 2FA setup
    And I log out
    And I log back in with my username and password
    Then I should be prompted for a TOTP code on the 2FA verification page
    And I should not be able to skip the 2FA step
  ```
- **Postconditions**: 2FA is required for all future logins

---

#### TC-ST-004: Redirect to Originally Requested Page After Login
- **Requirement**: After login, user is redirected to the page they originally tried to access
- **Priority**: Medium
- **Preconditions**:
  - User is not logged in
  - User attempts to navigate to a protected page (e.g., their repository settings)
- **Test Steps**:
  ```gherkin
  Scenario: Redirect to the originally requested URL after authentication
    Given I am not logged in to GitHub
    When I navigate to "https://github.com/settings/profile" (a protected page)
    Then I should be redirected to the login page
    And the return URL should be preserved
    When I enter valid credentials and click "Sign in"
    Then I should be redirected back to "https://github.com/settings/profile"
    And not to the generic GitHub dashboard
  ```
- **Postconditions**: User is on the originally requested page

---

## Test Coverage Matrix

| Requirement                              | Test Cases                     | Coverage Status |
|------------------------------------------|--------------------------------|-----------------|
| Login with valid username/password       | TC-F-001, TC-F-002             | ✓ Complete      |
| Two-factor authentication (TOTP)         | TC-F-003, TC-E-005, TC-ERR-007 | ✓ Complete      |
| Two-factor authentication (SMS)          | TC-F-004                       | ✓ Complete      |
| Recovery code login                      | TC-F-005, TC-ERR-008           | ✓ Complete      |
| SSO / OAuth login                        | TC-F-006                       | ✓ Complete      |
| Persistent session                       | TC-F-007                       | ✓ Complete      |
| Input validation (empty/boundary)        | TC-ERR-003–005, TC-E-001–004   | ✓ Complete      |
| Incorrect credentials handling           | TC-ERR-001, TC-ERR-002         | ✓ Complete      |
| Rate limiting / account lockout          | TC-ERR-006                     | ✓ Complete      |
| HTTPS enforcement                        | TC-ERR-009                     | ✓ Complete      |
| Session expiry                           | TC-ERR-010                     | ✓ Complete      |
| Logout and re-login                      | TC-ST-001                      | ✓ Complete      |
| Password change invalidates sessions     | TC-ST-002                      | ✓ Complete      |
| 2FA enabled mid-session                  | TC-ST-003                      | ✓ Complete      |
| Post-login redirect to original URL      | TC-ST-004                      | ✓ Complete      |

---

## Notes
- Error messages for invalid username vs. invalid password are intentionally identical (`"Incorrect username or password."`) — this is a deliberate security design to prevent username enumeration attacks (TC-ERR-001 and TC-ERR-002 verify this behavior)
- Rate-limiting thresholds (TC-ERR-006) may vary; the exact number of allowed attempts before lockout/CAPTCHA trigger should be confirmed with GitHub's current policy
- TOTP clock skew tolerance (TC-E-005) is typically ±1 code window (30 seconds), which GitHub generally supports
- Recovery codes (TC-F-005) are one-time use; GitHub generates 16 codes on 2FA setup
- SAML SSO tests (TC-F-006) require an enterprise GitHub organization with SSO configured and cannot be tested on a personal account
