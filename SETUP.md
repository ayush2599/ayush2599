# Set up your GitHub profile README

The only file you normally edit is `data/profile.yml`. The automation turns it into the visible sections of `README.md` and updates the animated header.

## 1. Personalize it locally

1. Open `data/profile.yml`.
2. Replace `YOUR_GITHUB_USERNAME`, `YOUR_LINKEDIN_SLUG`, and `YOUR_EMAIL`.
3. Rewrite the current focus, current projects, capabilities, and outside-the-terminal text so every claim is yours.
4. From the package folder, run:

   ```powershell
   py -m pip install -r requirements.txt
   py scripts/update-readme.py
   ```

5. Open `README.md` to review the result. Do not remove any `profile:`, `START_SECTION`, or `END_SECTION` comments; the automations use them as anchors.

If you do not want LinkedIn or email shown, delete that line from `links` in `data/profile.yml`. Placeholder links are hidden automatically after the renderer runs.

## 2. Create the special GitHub repository

1. On GitHub, select **New repository**.
2. The repository name must be **exactly your GitHub username**, including capitalization. For example, the account `octocat` needs a repository named `octocat`.
3. Set the repository to **Public**. A private repository will not appear as your profile README.
4. You may leave GitHub's “Add a README” option off because this package already contains one.
5. Create the repository.

## 3. Upload the package

Upload the **contents** of `github-profile-readme` to the repository root—not the enclosing folder. After upload, GitHub should show this shape:

```text
YOUR_GITHUB_USERNAME/
├── .github/workflows/update-profile.yml
├── .github/workflows/snake.yml
├── assets/hero.svg
├── data/profile.yml
├── scripts/update-readme.py
├── README.md
└── requirements.txt
```

You can upload through GitHub's web interface, GitHub Desktop, or Git. Commit everything to the default `main` branch.

## 4. Enable Actions

1. Open the repository's **Actions** tab and approve workflows if GitHub asks.
2. Go to **Settings → Actions → General**.
3. Under **Workflow permissions**, select **Read and write permissions**, then save.
4. Return to **Actions**.
5. Open **Update profile**, choose **Run workflow**, and run it.
6. Open **Generate contribution snake**, choose **Run workflow**, and run it.
7. Give the first snake run a minute or two. It creates an `output` branch; refresh your profile after it finishes.

Both workflows also run daily. GitHub can disable scheduled workflows in a public repository after 60 days without repository activity; if that happens, re-enable them from the Actions tab or run them manually.

## 5. Optional WakaTime section

The profile works without WakaTime. To enable it:

1. Create a WakaTime account and install its editor plugin.
2. In this repository, go to **Settings → Secrets and variables → Actions**.
3. Create a repository secret named exactly `WAKATIME_API_KEY` and paste your WakaTime API key as its value.
4. Run **Update profile** again.

Never paste the API key into `profile.yml`, `README.md`, or a workflow file.

## Everyday updates

Edit `data/profile.yml` on GitHub and commit it. The push triggers **Update profile**, which regenerates the README and header. The recent-activity block, optional WakaTime block, rotating developer joke, and contribution snake then maintain themselves.

## Quick troubleshooting

- **README is not on the profile:** confirm the repository is public, its name exactly matches the username, and `README.md` is in the root.
- **Action cannot push:** set Workflow permissions to Read and write, then rerun it.
- **Snake is blank:** run the snake workflow once, confirm the `output` branch exists, and confirm `github_username` has no placeholder left.
- **A link is missing:** placeholder links are hidden deliberately; add the real URL in `data/profile.yml` and rerun the renderer.
- **Schedule stopped:** GitHub may disable schedules after prolonged repository inactivity; manually re-enable the workflow.
