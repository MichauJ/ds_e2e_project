1. Update your local main branch:
   git checkout main
   git pull origin main

2. Create a new feature branch:
   git checkout -b feat/training_pipeline

3. Confirm you are on the correct branch:
   git status

4. Start working on your changes in the code

5. Stage your changes:
   git add .

6. Commit your changes:
   git commit -m "Describe your changes"

7. Push your branch to remote:
   git push -u origin feat/training_pipeline

8. Continue making changes and repeat steps 5–7 as needed

9. Open a Pull Request from feat/training_pipeline to main when ready

10. After the PR is merged, update main again:
    git checkout main
    git pull origin main