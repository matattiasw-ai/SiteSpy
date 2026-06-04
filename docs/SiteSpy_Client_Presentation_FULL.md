# SiteSpy Client Presentation FULL

PowerPoint: `docs/SiteSpy_Client_Presentation_FULL.pptx`
Prepared: 7 June 2026

## Source Notes

- The presentation is based on repository files, screen source, services, Firebase rules, app configuration, and collaborator documentation.
- Runtime browser screenshots were not available in this environment, so the deck uses polished UI walkthrough visual assets generated from implemented screen names, fields, actions, and theme colors.
- No current-feature claims are made beyond repository evidence listed per slide.

## Slide 1: SiteSpy System Presentation

Content:
- Client Demonstration and Technical Overview
- Prepared for Group 2 / client team
- 7 June 2026
Images used:
- `assets/social-preview.png`
Speaker notes: Open by introducing SiteSpy as the mobile-first estimation system built for the student/client team.
Evidence files:
- `README.md`
- `app.json`
- `assets/logo-mark-transparent.png`

## Slide 2: Executive Summary

Content:
- SiteSpy is an Expo React Native Android app for masonry wall project estimation.
- The app supports sign-in, project records, manual estimates, image records, and BOQ-style summaries.
- Firebase stores user-owned project, estimate, and wall-image records with owner-based access rules.
- The repository includes collaborator ownership, testing, Firebase setup, and final submission documentation.
Images used:
- `assets/social-preview.png`
Speaker notes: Summarize the system in plain language before going deeper.
Evidence files:
- `README.md`
- `docs/User_Manual.md`

## Slide 3: Presentation Roadmap

Content:
- Problem and project objectives
- Solution overview and target users
- App walkthrough and core workflows
- Architecture, Firebase, data, and security
- Member contributions and Git workflow
- Testing, build process, demo script, and Q&A
Images used:
- `docs/presentation-assets/diagrams/member-workstream-map.png`
Speaker notes: Set expectations for the presentation.
Evidence files:
- `docs/collaborators/task-allocation.md`

## Slide 4: Problem Statement

Content:
- Manual construction estimation can be slow, inconsistent, and difficult to present clearly.
- Students need visible ownership across a shared project and assigned branches.
- Project records must be stored securely and tied to the correct signed-in user.
- Presenters need a technical explanation that is accurate and understandable.
Speaker notes: Explain the client problem before naming features.
Evidence files:
- `README.md`

## Slide 5: Project Objectives

Content:
- Build a mobile-first Android app using Expo and React Native.
- Use Firebase for authentication and user-owned backend records.
- Support project creation, manual estimation, image records, and report-ready summaries.
- Document collaborator responsibilities, branches, testing, and final submission steps.
- Prepare the project for Android demonstration and continued student work.
Speaker notes: Link each objective to a visible part of the app or repository.
Evidence files:
- `README.md`
- `docs/Testing_Checklist.md`

## Slide 6: What SiteSpy Does

Content:
- The user signs in to a protected workspace.
- The user creates a project for a wall or construction task.
- The app captures wall dimensions, unit type, prices, and labour values.
- The calculation workflow produces unit counts, mortar allowance, labour, and total cost.
- Saved projects and estimates can be reviewed later through history and detail screens.
Images used:
- `docs/presentation-assets/screenshots/dashboard.png`
Speaker notes: Describe the app as a sequence of actions.
Evidence files:
- `docs/User_Manual.md`

## Slide 7: Target Users and Use Cases

Content:
- Students presenting a working mobile app and team contribution structure.
- Small builders or estimators who need quick wall quantity and cost estimates.
- Demonstration panel members reviewing system design, quality, and maintainability.
- Future maintainers continuing from documented branches and service boundaries.
Speaker notes: Emphasize the demo and maintainability use cases.
Evidence files:
- `README.md`

## Slide 8: Basic Programming Concepts

Content:
- Frontend: the visible mobile interface users tap and read.
- Screens: full views such as Login, Dashboard, Manual Estimate, Project Details, and Settings.
- Components: reusable UI pieces such as cards, buttons, headers, inputs, and status states.
- Services: modules that connect screens to Firebase, storage, reports, and calculations.
- Database: Firestore collections that store user-owned app records.
- Build process: commands that prepare the app for local use and Android delivery.
Speaker notes: Help non-technical presenters explain the implementation.
Evidence files:
- `src/components`
- `src/screens`
- `src/services`

## Slide 9: Technology Stack

Content:
- Expo Managed Workflow and React Native for Android app delivery.
- JavaScript and JSX for screens, services, components, and utilities.
- React Navigation for auth flow, bottom tabs, project stack, and profile stack.
- Firebase Auth, Firestore, and Storage for backend behaviour.
- EAS Build profiles for preview APK and production app-bundle paths.
- Expo image, font, file-system, image-manipulator, and build-properties libraries.
Speaker notes: Keep this grounded in package.json and app configuration.
Evidence files:
- `package.json`
- `app.json`
- `eas.json`

## Slide 10: App Feature Map

Images used:
- `docs/presentation-assets/diagrams/app-feature-map.png`
Speaker notes: Walk through each feature around the center of the map.
Evidence files:
- `README.md`
- `src/navigation/MainTabs.js`

## Slide 11: High-Level Architecture Diagram

Images used:
- `docs/presentation-assets/diagrams/high-level-architecture.png`
Speaker notes: Explain the split between mobile UI, services, Firebase, and configuration.
Evidence files:
- `src/navigation`
- `src/services`

## Slide 12: Navigation Architecture

Images used:
- `docs/presentation-assets/diagrams/navigation-architecture.png`
Speaker notes: Show that signed-out and signed-in users have different navigation paths.
Evidence files:
- `src/navigation/AppNavigator.js`
- `src/navigation/MainTabs.js`

## Slide 13: Data Flow Diagram

Images used:
- `docs/presentation-assets/diagrams/data-flow.png`
Speaker notes: Explain the estimate save workflow and image record path.
Evidence files:
- `src/services/projectService.js`
- `src/services/estimateService.js`

## Slide 14: Firebase Architecture

Images used:
- `docs/presentation-assets/diagrams/firebase-architecture.png`
Speaker notes: Connect Auth, Firestore collections, Storage paths, and owner rules.
Evidence files:
- `docs/Firebase_Setup_Guide.md`
- `firestore.rules`
- `storage.rules`

## Slide 15: Database / Collection Design

Images used:
- `docs/presentation-assets/diagrams/database-model.png`
Speaker notes: Explain each collection and how project-linked records are connected.
Evidence files:
- `shared/data-model.md`

## Slide 16: Security Model

Content:
- Firestore rules require authentication before app records can be read or written.
- Project, estimation, and wall-image records are restricted to the matching userId.
- Storage paths are scoped to the authenticated user.
- The project check blocks private files such as environment values, credentials, tokens, and raw collaborator secrets.
- Firebase values are kept in local .env and loaded through app configuration.
Speaker notes: Present this as a practical data protection story.
Evidence files:
- `firestore.rules`
- `storage.rules`
- `scripts/project-check.js`

## Slide 17: Folder and Codebase Structure

Content:
- src/navigation: auth gate, stacks, and bottom tabs.
- src/screens: auth, dashboard, project, estimate, image, profile, and settings screens.
- src/components: shared mobile UI building blocks.
- src/services: Firebase, project, storage, report, auth, and estimate services.
- src/utils and src/theme: calculations, validation, formatting, colors, spacing, typography.
- docs, assets, functions, hosting, and Firebase config files support delivery and documentation.
Speaker notes: Make clear that the repo separates responsibilities.
Evidence files:
- `README.md`

## Slide 18: User Flow Walkthrough

Content:
- Splash opens while startup state is checked.
- Signed-out users choose login, account creation, or password recovery.
- Signed-in users land in Dashboard and navigate through bottom tabs.
- New Project starts a project file and moves into estimation.
- Manual Estimate saves calculations and Estimate Summary presents BOQ lines.
- Image Estimate records a wall image and reference measurement.
- Profile and Settings close the demo with account and app information.
Images used:
- `docs/presentation-assets/diagrams/data-flow.png`
Speaker notes: Use this as the presenter app walkthrough map.
Evidence files:
- `docs/User_Manual.md`

## Slide 19: Screenshot Walkthrough 1 - Authentication

Content:
- Splash prepares app startup.
- Login supports email/password and email-link sign-in.
- Register creates a Firebase-backed account profile.
- Forgot Password sends a Firebase reset email.
Images used:
- `docs/presentation-assets/screenshots/splash.png`
- `docs/presentation-assets/screenshots/login.png`
Speaker notes: Show the sign-in path before protected app screens.
Evidence files:
- `src/screens/LoginScreen.js`

## Slide 20: Screenshot Walkthrough 2 - Dashboard and Projects

Content:
- Dashboard summarizes projects, estimations, masonry units, and total estimate value.
- Project History lists saved project files.
- Project Details connects project notes, saved estimates, image records, and actions.
Images used:
- `docs/presentation-assets/screenshots/dashboard.png`
- `docs/presentation-assets/screenshots/project-history.png`
Speaker notes: Explain how the user finds and reopens work.
Evidence files:
- `src/screens/DashboardScreen.js`

## Slide 21: Screenshot Walkthrough 3 - Estimation Workflow

Content:
- New Project captures the field file.
- Manual Estimate collects wall and costing inputs.
- Estimate Summary presents BOQ-style line items and totals.
Images used:
- `docs/presentation-assets/screenshots/new-project.png`
- `docs/presentation-assets/screenshots/manual-estimate.png`
Speaker notes: Walk through creating an estimate from start to saved result.
Evidence files:
- `src/screens/ManualEstimateScreen.js`

## Slide 22: Screenshot Walkthrough 4 - Image Estimate and Records

Content:
- The image screen supports gallery or camera selection.
- A real reference measurement is captured with the image record.
- The app stores image metadata linked to the project and user.
Images used:
- `docs/presentation-assets/screenshots/image-estimate.png`
- `docs/presentation-assets/screenshots/project-details.png`
Speaker notes: Clarify the image record path and reference measurement.
Evidence files:
- `src/screens/ImageEstimateScreen.js`

## Slide 23: Screenshot Walkthrough 5 - Profile and Settings

Content:
- Profile shows account identity details.
- Settings includes preferences and Android target information.
- Logout clears the signed-in session and sensitive local state.
Images used:
- `docs/presentation-assets/screenshots/profile.png`
- `docs/presentation-assets/screenshots/settings.png`
Speaker notes: End the demo with account control and sign-out.
Evidence files:
- `src/screens/ProfileScreen.js`

## Slide 24: Estimation Logic Explained

Images used:
- `docs/presentation-assets/diagrams/estimation-logic.png`
Speaker notes: Explain formulas in simple terms: inputs become quantities, quantities become costs, costs become the summary.
Evidence files:
- `src/utils/calculations.js`

## Slide 25: BOQ / Report Summary Explained

Content:
- Masonry units are listed as a material line item.
- Mortar allowance is calculated and priced separately.
- Labour is calculated from wall area and labour rate.
- The total cost is the sum of material, mortar, and labour costs.
- The summary format helps presenters discuss project cost in a structured way.
Images used:
- `docs/presentation-assets/screenshots/estimate-summary.png`
Speaker notes: Explain the result card and line-item value.
Evidence files:
- `src/utils/calculations.js`

## Slide 26: Collaboration System

Content:
- Collaborator mapping stores names, GitHub identities, emails, and departments where recorded.
- Task allocation maps each student to a branch, workstream, contribution area, and deliverable.
- Git workflow notes define branch and pull request expectations.
- Private values such as passwords and tokens are redacted and excluded from presentation content.
Images used:
- `docs/Collaborators_Departments.jpeg`
Speaker notes: Tie collaboration documentation to clean handoff and presentation readiness.
Evidence files:
- `docs/Collaborators.json`
- `docs/collaborators/task-allocation.md`

## Slide 27: Git Workflow

Images used:
- `docs/presentation-assets/diagrams/git-workflow.png`
Speaker notes: Explain pull, branch, check, commit, push, and review.
Evidence files:
- `docs/collaborators/git-workflow.md`

## Slide 28: Member Contribution Overview

Content:
- All documented members are mapped to branch ownership and contribution areas.
Speaker notes: Use this as the transition into individual member contribution slides.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`

## Slide 29: Member Contribution: Tunacky Kandere

Content:
- GitHub / identity: tunackykandere-lab
- Branch: mobile/kandere-ndl-navigation-shell
- Area: Navigation shell and app layout
- Auth-gated navigation structure
- Bottom-tab and stack layout
- Android portrait app flow
- makes the app easy to move through
- separates auth, project, and profile workflows
Images used:
- `docs/presentation-assets/member-slides/tunacky-kandere.png`
Speaker notes: Explain that this contribution supports makes the app easy to move through.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 30: Member Contribution: Kavakuru Metarere

Content:
- GitHub / identity: Kavakuru-Metarere7
- Branch: mobile/metare-k-auth-screens
- Area: Authentication screens
- Login, register, and recovery screens
- Validation-ready account entry
- Firebase sign-in actions
- protects access to user-owned records
- gives the demo a complete account flow
Images used:
- `docs/presentation-assets/member-slides/kavakuru-metarere.png`
Speaker notes: Explain that this contribution supports protects access to user-owned records.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 31: Member Contribution: Nambuli NN

Content:
- GitHub / identity: documented branch owner
- Branch: mobile/nambuli-nn-dashboard
- Area: Dashboard experience
- Project metrics
- Recent projects
- Empty and loading states
- shows system value immediately after sign-in
- turns saved data into presentation metrics
Images used:
- `docs/presentation-assets/member-slides/nambuli-nn.png`
Speaker notes: Explain that this contribution supports shows system value immediately after sign-in.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 32: Member Contribution: Mathias Jonas

Content:
- GitHub / identity: Mathias4040
- Branch: mobile/jonas-mm-project-history
- Area: Project history and details
- Saved project browsing
- Detail review
- Edit/delete and estimate visibility
- lets users reopen and manage saved field files
- connects estimates and images to each project
Images used:
- `docs/presentation-assets/member-slides/mathias-jonas.png`
Speaker notes: Explain that this contribution supports lets users reopen and manage saved field files.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 33: Member Contribution: Emilly Ndapuka

Content:
- GitHub / identity: emilly20-06
- Branch: mobile/ndapuka-eii-manual-estimation
- Area: Manual estimation forms
- Wall input experience
- Calculation preview
- Save estimate flow
- turns construction inputs into repeatable calculations
- supports the main value of the app
Images used:
- `docs/presentation-assets/member-slides/emilly-ndapuka.png`
Speaker notes: Explain that this contribution supports turns construction inputs into repeatable calculations.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 34: Member Contribution: Amalia Mangundu

Content:
- GitHub / identity: amaliamangundu-tech
- Branch: mobile/mangundu-a-profile-settings
- Area: Profile and settings
- Account view
- Settings screen
- Logout path
- gives users account control and logout access
- rounds out the protected app experience
Images used:
- `docs/presentation-assets/member-slides/amalia-mangundu.png`
Speaker notes: Explain that this contribution supports gives users account control and logout access.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 35: Member Contribution: Johannes Kandjeke

Content:
- GitHub / identity: Kandjekejohannes54
- Branch: mobile/kandjeke-jm-responsive-testing
- Area: Android responsive testing
- Portrait spacing
- Keyboard behaviour
- Touch-target checks
- improves readability on portrait Android screens
- supports reliable live demonstration
Images used:
- `docs/presentation-assets/member-slides/johannes-kandjeke.png`
Speaker notes: Explain that this contribution supports improves readability on portrait Android screens.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 36: Member Contribution: Hilma Shuumbwa

Content:
- GitHub / identity: hilma-shuumbwa
- Branch: firebase/shuumbwa-hmn-project-setup
- Area: Expo and Firebase setup
- Firebase config
- Expo app settings
- Android package setup
- provides the foundation for app startup and backend connection
- makes configuration traceable
Images used:
- `docs/presentation-assets/member-slides/hilma-shuumbwa.png`
Speaker notes: Explain that this contribution supports provides the foundation for app startup and backend connection.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 37: Member Contribution: Petrus Hamukwaya

Content:
- GitHub / identity: ramuntu
- Branch: firebase/hamukwaya-pnp-auth-rules
- Area: Authentication rules
- Auth behaviour
- Account ownership
- Protected record assumptions
- keeps sign-in behaviour aligned with Firebase Auth
- supports secure account-linked data
Images used:
- `docs/presentation-assets/member-slides/petrus-hamukwaya.png`
Speaker notes: Explain that this contribution supports keeps sign-in behaviour aligned with Firebase Auth.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 38: Member Contribution: Karl Hamberera

Content:
- GitHub / identity: Karlhamberera
- Branch: firebase/hamberera-mkp-firestore-models
- Area: Firestore data model
- Collection structure
- Owner fields
- Linked records
- defines how records are organized and linked
- supports project history and summaries
Images used:
- `docs/presentation-assets/member-slides/karl-hamberera.png`
Speaker notes: Explain that this contribution supports defines how records are organized and linked.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 39: Member Contribution: Washington Matattias

Content:
- GitHub / identity: matattiasw-ai
- Branch: firebase/matattias-w-integration-review
- Area: Repository and release review
- Integration checks
- Project check
- Release readiness
- keeps integration checks visible
- reduces risk before presentation and build
Images used:
- `docs/presentation-assets/member-slides/washington-matattias.png`
Speaker notes: Explain that this contribution supports keeps integration checks visible.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 40: Member Contribution: Klaudia Kambowe

Content:
- GitHub / identity: kambowe
- Branch: firebase/kambowe-kn-project-services
- Area: Project services
- Create/list/update/delete
- Project timestamps
- Linked estimates
- provides data operations behind project screens
- keeps screen code focused on user experience
Images used:
- `docs/presentation-assets/member-slides/klaudia-kambowe.png`
Speaker notes: Explain that this contribution supports provides data operations behind project screens.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 41: Member Contribution: Martha Heita

Content:
- GitHub / identity: marthandilimengungo-dotcom
- Branch: firebase/heita-mn-validation-errors
- Area: Validation and errors
- Form validation
- Clear user messages
- Retry/error states
- helps users correct mistakes before saving
- makes failures easier to explain and retry
Images used:
- `docs/presentation-assets/member-slides/martha-heita.png`
Speaker notes: Explain that this contribution supports helps users correct mistakes before saving.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 42: Member Contribution: Michael Kazundire

Content:
- GitHub / identity: IcyBeibi68023
- Branch: firebase/tjatindi-mk-security-review
- Area: Firebase rules review
- Firestore rules
- Storage paths
- Owner-only access
- protects records through owner-only rules
- supports a defensible security explanation
Images used:
- `docs/presentation-assets/member-slides/michael-kazundire.png`
Speaker notes: Explain that this contribution supports protects records through owner-only rules.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 43: Member Contribution: Beatha Haipumbu

Content:
- GitHub / identity: beathapawana-dot
- Branch: firebase/haipumbu-bnp-estimation-workflow
- Area: Estimation workflow
- Wall area
- Unit quantities
- Cost total
- connects form inputs to saved cost summaries
- supports the main construction-estimation use case
Images used:
- `docs/presentation-assets/member-slides/beatha-haipumbu.png`
Speaker notes: Explain that this contribution supports connects form inputs to saved cost summaries.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 44: Member Contribution: Valentina Correia

Content:
- GitHub / identity: Valentina-Correia
- Branch: firebase/correia-vp-summary-export
- Area: Summary formatting
- BOQ line items
- Cost breakdown
- Presenter-friendly totals
- makes calculation results easier to present
- turns estimates into BOQ-style outputs
Images used:
- `docs/presentation-assets/member-slides/valentina-correia.png`
Speaker notes: Explain that this contribution supports makes calculation results easier to present.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 45: Member Contribution: Hilda Iita

Content:
- GitHub / identity: next-GenCoder
- Branch: firebase/iita-hn-quality-checks
- Area: App checks
- Project check
- Testing checklist
- Export readiness
- confirms required files and quality commands
- supports final submission confidence
Images used:
- `docs/presentation-assets/member-slides/hilda-iita.png`
Speaker notes: Explain that this contribution supports confirms required files and quality commands.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 46: Member Contribution: Linus Shikongo

Content:
- GitHub / identity: Linus45-blid
- Branch: firebase/shikongo-lik-eas-deployment
- Area: EAS deployment
- Preview APK path
- Build profile
- Android delivery
- defines the Android APK delivery path
- supports installable demo readiness
Images used:
- `docs/presentation-assets/member-slides/linus-shikongo.png`
Speaker notes: Explain that this contribution supports defines the Android APK delivery path.
Evidence files:
- `docs/collaborators/task-allocation.md`
- `docs/Collaborators.json`
- `docs/collaborators/frontend-team.md`
- `docs/collaborators/backend-team.md`

## Slide 47: Testing and Quality Assurance

Content:
- npm run check verifies required files and blocks private or wrong-stack files.
- Expo Doctor is configured as npm run doctor for Expo project health checks.
- Android export is configured through npm run export:android.
- Testing checklist covers auth, project workflow, estimation, image workflow, and Android UI.
- Firebase rules and storage paths are reviewed as part of the quality story.
Images used:
- `docs/presentation-assets/diagrams/build-deployment-flow.png`
Speaker notes: Show that quality is both automated and documented.
Evidence files:
- `package.json`
- `scripts/project-check.js`
- `docs/Testing_Checklist.md`

## Slide 48: Debugging Work Completed

Content:
- The repository includes crash logs before and after fixes.
- Runtime configuration has guard behaviour for missing Firebase values.
- Auth state initialization shows a splash screen before routing.
- Project check confirms required files and secret-safety expectations.
- Final submission checklist tracks Expo Go, EAS, Firebase, and branch readiness.
Speaker notes: Explain the debugging work as evidence of review and stabilization.
Evidence files:
- `sitespy-crash-log.txt`
- `sitespy-crash-log-after-fix.txt`
- `src/services/runtimeConfig.js`

## Slide 49: How to Run the Project

Content:
- Install dependencies: npm install
- Create local environment file: cp .env.example .env
- Start Expo: npm start
- Run Android target: npm run android
- Run project check: npm run check
- Run Expo Doctor: npm run doctor
- Export Android bundle: npm run export:android
- Build preview APK: npm run build:apk
Speaker notes: Use this as the presenter technical runbook.
Evidence files:
- `package.json`
- `README.md`

## Slide 50: How Students Continue Work

Content:
- Configure Git identity with the student’s own name and email.
- Check out the assigned branch from the task-allocation document.
- Work only on the assigned app section or service area.
- Run checks before committing.
- Push the branch and prepare review evidence.
- Use portfolio notes to explain contribution, learning, challenges, and validated files.
Images used:
- `docs/presentation-assets/diagrams/git-workflow.png`
Speaker notes: Connect Git workflow to individual contribution evidence.
Evidence files:
- `docs/collaborators/git-workflow.md`
- `README.md`

## Slide 51: Demo Script for Monday

Content:
- Introduce SiteSpy as a mobile-first wall-estimation app.
- Explain the estimation and collaboration problem.
- Show login and account flow.
- Show dashboard and project history.
- Create or open a project.
- Run a manual estimate and show the BOQ summary.
- Show image estimate and project details.
- Explain Firebase, data model, and security.
- Summarize member contributions.
- Close with testing, build readiness, and Q&A.
Speaker notes: This slide can be rehearsed directly as the demo script.
Evidence files:
- `docs/User_Manual.md`

## Slide 52: Likely Questions and Answers

Content:
- What problem does SiteSpy solve? It makes wall project estimates and saved records easier to produce and present.
- Why mobile-first? The app is designed for Android field-style use and student demonstration.
- Why Firebase? It provides authentication, Firestore records, storage paths, and deployable rules.
- How is user data protected? Rules require authentication and matching user ownership.
- How does estimation work? Wall dimensions and rates are converted into unit, mortar, labour, and total cost values.
- Can the app expand? Future work can add reporting, offline mode, and additional estimation types.
- How was it tested? Through project checks, testing checklist coverage, Expo checks, and Android export path.
Speaker notes: Use this to prepare presenters for panel questions.
Evidence files:
- `README.md`
- `docs/Testing_Checklist.md`

## Slide 53: Future Improvements

Content:
- PDF report export for saved estimates.
- Additional construction estimation types beyond masonry walls.
- Offline mode for field use without consistent network access.
- Admin or reviewer mode for classroom assessment.
- Improved image measurement workflows.
- More reporting, charts, and portfolio evidence exports.
Speaker notes: Be clear that these are future improvements, not current claims.
Evidence files:
- `README.md`
- `docs/User_Manual.md`

## Slide 54: Conclusion

Content:
- SiteSpy is a working mobile-first estimation app built with Expo React Native.
- The app supports Firebase-backed user records, projects, estimates, images, and summaries.
- The codebase separates screens, components, services, utilities, theme, and configuration.
- The collaboration structure documents member ownership and branch responsibilities.
- The team can present the app workflow, technical architecture, and individual contributions clearly.
Images used:
- `assets/social-preview.png`
Speaker notes: Close by restating the system, foundation, and team contribution story.
Evidence files:
- `README.md`
- `docs/collaborators/task-allocation.md`

## Slide 55: Thank You

Content:
- SiteSpy: secure mobile estimation and project records for the client team.
Images used:
- `assets/logo-mark-transparent.png`
Speaker notes: Invite questions and move into live demo or panel discussion.
Evidence files:
- `assets/logo-mark-transparent.png`

## Commands Verified

- `npm run check`
- `npm run doctor`
- `npm run export:android`
- Firebase deploy attempt is reported in the final implementation summary when credentials and tooling allow it.

## Final File List

- `docs/SiteSpy_Client_Presentation_FULL.pptx`
- `docs/SiteSpy_Client_Presentation_FULL.md`
- `docs/presentation-assets`
- `docs/presentation-assets/diagrams`
- `docs/presentation-assets/screenshots`
- `docs/presentation-assets/member-slides`