# Offline Assistant — Project Scope

## Objectives

The primary user is me, Kate. I want an offline assistant that can help me find, understand, and summarize information stored on my computer and connected external storage devices, such as USB drives and microSD cards. The long-term goal is to build an assistant that works similarly to an online chatbot, but can still provide useful information when internet access is unavailable.

Eventually, I would like the assistant to work across many types of local information, including documents, text files, images through OCR, video transcripts, and offline reference libraries such as `.zim` files used with Kiwix. I would also like to continue expanding it after this class so that it can organize and retrieve information collected from multiple devices and sources.

For this class, the first version will focus on retrieving useful information from a limited set of approved local documents and returning an answer with the source information it used.

Example questions:

1. How do I purify drinking water if I do not have access to running water?
2. Find the instructions I saved for using my generator and summarize the startup procedure.
3. What information do I have stored about treating a minor wound, and which document did it come from?

## The gap / need

Right now, I have useful information spread across my computer, external storage devices, downloaded reference libraries, saved documents, photos, videos, and other files. When I need something, I usually have to remember where I saved it, search folders manually, open files one by one, or use a separate program such as Kiwix for `.zim` reference material. This becomes especially inconvenient when internet access is unavailable and I cannot rely on an online search engine or cloud-based chatbot.

Document retrieval is a better fit for this project than a traditional database, form, or dashboard because the information I want to search is mostly unstructured. It lives inside documents and other content rather than in neat rows and columns. I want to be able to ask a natural-language question and have the assistant locate the most relevant stored information, summarize it, and tell me which source it came from.

A database or dashboard would work well for structured information such as inventories, dates, or quantities, but it would not be as useful for searching instructions, reference guides, notes, transcripts, and other long-form material. Retrieval lets the assistant search across those sources without requiring me to manually organize every piece of information into a fixed database structure first.

## Key deliverables

The smallest worthwhile version of this project is an offline assistant that can search a limited collection of approved local documents, identify the most relevant information, and return a concise answer with the source it used.

For this class, the first version should be able to:

- load a small local document collection from the computer
- accept a natural-language question
- retrieve the most relevant document or passages
- generate a short answer grounded only in the retrieved sources
- show the source file so I can verify where the answer came from
- work without requiring an internet connection for the core retrieval workflow

One feature I will intentionally leave out of the first version is automatic ingestion of everything I browse online. That feature is part of the long-term vision, but it would require additional work around browser integration, permissions, privacy, source tracking, storage, and deciding what information should be retained.

## Current scope boundary

The class project will intentionally stay smaller than the long-term vision. The working prototype will use a limited set of approved local documents and focus on retrieval, concise answers, and source citation. Broad device-wide indexing, automatic browser capture, unrestricted file-format support, continuous background ingestion, and fully autonomous memory are outside the first version unless time and course requirements allow them later.

## Future expansion

The long-term goal is to develop this into a more capable offline personal assistant that can search and reason across information stored on the computer and connected storage devices. Future versions could support a wider range of sources, including documents, images through OCR, video transcripts, `.zim` archives used with Kiwix, and other locally stored reference material.

I would also like to explore ways for the assistant to build a local knowledge collection from information I intentionally save while browsing online, so useful material can remain available later when internet access is unavailable. Any future version would need clear controls for privacy, permissions, storage limits, source tracking, and deciding what information should or should not be retained.

## Data requirements & constraints

For the class version, the assistant will use only synthetic, sanitized, personally owned, or publicly available documents that I intentionally place in an approved local data folder. Only files deliberately placed in that approved source folder will be indexed.

The repository and agent prompts must not contain passwords, API keys, private credentials, sensitive personal information, employer or client confidential material, or export-controlled information. I will also avoid giving the class version unrestricted access to my entire computer or external drives.

To maintain this boundary, I will review files before adding them. Environment files, credentials, and private folders will remain excluded from Git and from the assistant's retrieval collection.

For future versions, I would like to expand support to additional local sources such as `.zim` archives, OCR-extracted text, image metadata, and video transcripts, but only with clear user-controlled permissions and source tracking.

## Success measure

The first version will be considered successful if the assistant can answer questions using only the approved local document collection and clearly identify the source material used for each answer.

I will test the assistant with a small set of questions whose answers are known to exist in the local documents. For each question, the assistant should retrieve the correct source, provide an answer that matches the source, and include a citation or source filename that I can verify manually.

A reasonable pass threshold for the class version is at least **4 out of 5 supported questions answered correctly with the correct source identified**.

Example supported test questions:

- How do I purify drinking water?
- What are the startup steps for the generator?
- What information is stored about treating a minor wound?
- Which document contains information about food storage?
- What does the reference material say about emergency lighting?

I will also include at least one unsupported question:

**What is tomorrow's weather forecast?**

If that information is not present in the approved local documents, the assistant should say that it does not know or that the information is not available in its local sources rather than inventing an answer.

## Peer review and revision

Peer review is pending. Mike and I worked together for roughly four hours on Arena testing and development during an earlier working session. I sent him the scoping draft for asynchronous review and will update this section with his actual feedback and any resulting revision once it is received.
