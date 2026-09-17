# Prof. Kern Tutoring

This is the GitHub Pages site for Prof. Kern Tutoring.

## Files
- `index.html` — home page with lesson format, policies, billing, and collaboration information
- `about.html` — about page
- `schedule.html` — schedule a session page
- `contact.html` — contact page
- `styles.css` — styling
- `script.js` — mobile navigation

## Important
The Contact form opens the visitor's email client and addresses the message to
`zoekern@gmail.com`.

The Schedule a Session page embeds:
`https://koalendar.com/e/tutoring-with-zoe`

## Local development

Python 3 is the only local dependency. Start the development server from this folder:

```powershell
python dev-server.py
```

Open `http://127.0.0.1:8000` in a browser. Changes to `index.html`, `styles.css`, or `script.js` are detected automatically and reload the page. Press `Ctrl+C` in the server terminal to stop it.

## GitHub Pages deployment

The `CNAME` file configures the site for `www.zoekay.com`. In the GitHub repository, open **Settings > Pages**, choose **Deploy from a branch**, select `main` and `/ (root)`, and save.

At the domain provider, create a CNAME record for `www` pointing to `sunkiss115.github.io`. Enable **Enforce HTTPS** in GitHub Pages after DNS finishes propagating.
