Spaceships in GCS
===

This is a GCS library that implements GURPS Spaceships.
It intends to use rules and content from the GURPS Spaceships line and related
Pyramid articles to allow GCS users to build spaceships as characters,
calculating relevant statistics using GCS' built-in scripting engine.

The general design philosophy is to provide a library of gcs equipment items,
which, when arranged together on a character sheet, fully describes a
spaceship. Wherever possible, anything that affects the cost, weight, or
capabilities of an equipment item should be _inside_ the equipment item. This
makes it easier to:
1. Reason about the data model - cycles can easily confuse the reader *and* the
   scripting engine.
2. Provide systems and modifiers in a way that could be sold in a shop.

It *may* diverge from rules as-written (e.g. modifiers applied to a ship that
affects its cost may be applied to the systems that make up the ship instead).
I will endeavour to make these divergences stated clearly, to prevent confusion
when comparing to the contents of GURPS Spaceships or related Pyramid articles.

Policy on Generative AI
---

![https://samvieten.itch.io/no-ai](no_ai_vector_sign_black.svg)

I will never knowingly use Generative AI in this project, and would encourage others to do likewise.

GURPS Game Aids copyright notice
---
GURPS is a trademark of Steve Jackson Games, and its rules and art are
copyrighted by Steve Jackson Games. All rights are reserved by Steve Jackson
Games. This game aid is the original creation of Jonathan Maw and is released
for free distribution, and not for resale, under the permissions granted in the
[Steve Jackson Games Online
Policy](http://www.sjgames.com/general/online_policy.html)


What is this License
---

This project is shared under the Aladdin Free Public License. One of the
stipulations of Steve Jackson Games on the distribution of Game Aids is that
they can't be used for commerical purposes, and the AFPL respects this right.
