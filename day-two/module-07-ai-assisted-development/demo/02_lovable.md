# Run sheet: Lovable

The live demo for section 2. Lovable builds a whole web app from a description, with a database and sign-in, and hosts it. Record the run beforehand: a build takes a few minutes, and the app is different every time.

You need a Lovable account. The free plan gives 5 credits a day, which is enough for steps 1 to 3. Checked against Lovable's documentation on 23 November 2026.

## 1. Plan it

1. Start a new project. In the mode picker next to the chat input, choose **Plan**. Option+P on a Mac, or Alt+P on Windows, cycles through Build, Chat and Plan.
2. Paste:

   > Build a feedback board for customers of Dormouse, a smart thermostat. Customers sign in, post a problem, and vote for other people's posts. Our support team can mark a post as answered, with a reply.

3. Answer its questions. Read the plan in the Plan view, and change one thing in it, such as "Customers can't see who voted".
4. Click **Approve**. That switches to Build mode.

Point out: Plan mode changes no code. The plan is saved in the project, in `.lovable/plan/`, so the next person can see what was agreed.

## 2. Build it

1. Let Build mode work. It can take a few minutes.
2. Sign up in the preview, post a problem, and vote for it.

Point out: it made a database, sign-in and the pages, from one paragraph. The database and sign-in are Lovable's **built-in backend** (Lovable Cloud), which runs on Supabase and is on by default.

## 3. Change it by pointing

1. In the preview toolbar, choose **Select elements**, click the vote button and type: "Make this ember orange, #E8743B."
2. Choose **Edit text inline** and change the page heading. Text edits made this way don't use credits.

## 4. Tell it about the company

1. Open **Project settings → Instructions** and paste in the six files from `data/brain/`. Together they are about 7,300 characters; the limit is 10,000.
2. In Build mode: "Rewrite every piece of text on the board in our voice."

Point out: Instructions are Lovable's own place for what the company knows. Every tool in this module has one, and they are all different (section 6).

## 5. Ask without changing anything

1. Switch to **Chat** mode and ask: "Who can see a customer's email address?"

Point out: Chat mode reads the code and the database but never edits them. If you ask for a change, it offers a **Start building** card.

## 6. Check it and publish it

1. Open **More → Security** and click **Run deep scan**. It takes 3 to 15 minutes and looks at the app's code: access control, unprotected endpoints, leaked secrets.
2. Click **Publish**, top right. The app goes live at `your-app.lovable.app`, and a quick security scan runs on every publish.

Point out: Lovable says fixing what the scan finds is up to the app's owner. Module 8 looks at what happened when apps built this way were published without that.

## 7. Take the code with you

1. Connect GitHub from the project. Lovable creates a new repository and keeps it in sync both ways, on one branch.

Point out: the code is a normal React app. A developer can carry on in Claude Code or Cursor.
