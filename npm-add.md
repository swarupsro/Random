# PassGuardJS – npm Publish & Auto Publish Guide

## 1. GitHub থেকে Automatic npm Publish (Recommended)

সবচেয়ে professional পদ্ধতি হলো **GitHub Actions + npm Trusted Publishing** ব্যবহার করা।

এতে GitHub-এ `v0.1.1`, `v1.0.0` এর মতো tag push করলেই npm-এ package automatically publish হয়ে যাবে।

---

## Step 1: GitHub Workflow তৈরি করুন

Project root-এ নিচের file তৈরি করুন:

```text
.github/workflows/publish.yml
```

Content:

```yaml
name: Publish to npm

on:
  push:
    tags:
      - "v*"

permissions:
  contents: read
  id-token: write

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 22
          registry-url: https://registry.npmjs.org/

      - name: Install dependencies
        run: npm ci

      - name: Publish package
        run: npm publish
```

---

## Step 2: npm Trusted Publisher Configure করুন

npmjs.com → আপনার package → **Settings** → **Trusted Publishers**

GitHub Actions add করুন।

Configuration:

```text
Owner: swarupsro
Repository: PassGuardJS
Workflow: publish.yml
```

---

## Step 3: Release Process

Patch release:

```bash
npm version patch
git push
git push --tags
```

Example:

```text
0.2.2 → 0.2.3
```

---

Minor release:

```bash
npm version minor
git push
git push --tags
```

Example:

```text
0.2.2 → 0.3.0
```

---

Major release:

```bash
npm version major
git push
git push --tags
```

Example:

```text
0.2.2 → 1.0.0
```

---

## Recommended Workflow

```bash
npm version patch
git push
git push --tags
```

GitHub Actions বাকি সব কাজ করে দিবে।

---

# 2. GitHub-এ Code Update করার পর npm-এ নতুন Version Publish

একই version দ্বিতীয়বার publish করা যায় না।

তাই প্রথমে version increase করতে হবে।

Example:

বর্তমান version:

```text
0.2.2
```

Publish করার জন্য:

```bash
git pull
npm install
npm run build
npm run test
npm version patch
npm publish
```

এতে version হবে:

```text
0.2.2 → 0.2.3
```

---

তারপর GitHub-এ push করুন:

```bash
git push
git push --tags
```

---

## Verify Published Version

```bash
npm view passguardjs version
```

---

## Install Test

```bash
npm install passguardjs@latest
```

---

## যদি বড় Feature যোগ করেন

```bash
npm version minor
npm publish
```

Example:

```text
0.2.2 → 0.3.0
```

---

## যদি Breaking Change হয়

```bash
npm version major
npm publish
```

Example:

```text
0.2.2 → 1.0.0
```

---

# Summary

### Manual Publish

```bash
npm version patch
npm publish
git push
git push --tags
```

---

### Automatic Publish (GitHub Actions)

```bash
npm version patch
git push
git push --tags
```

GitHub Actions automatically npm-এ publish করবে।

---

## Versioning Cheat Sheet

| Command | Example |
|----------|---------|
| `npm version patch` | 0.2.2 → 0.2.3 |
| `npm version minor` | 0.2.2 → 0.3.0 |
| `npm version major` | 0.2.2 → 1.0.0 |

---

## Best Practice

- Bug Fix → `patch`
- New Feature → `minor`
- Breaking Change → `major`
- Release-এর আগে সবসময়:
  - `npm run lint`
  - `npm test`
  - `npm run build`
- Production-এর জন্য **GitHub Actions + npm Trusted Publishing** ব্যবহার করুন।