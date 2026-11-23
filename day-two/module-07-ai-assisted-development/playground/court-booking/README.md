# Court booking

Build a booking page for a tennis club with four courts: members sign in and book an hour, nobody can book the same court twice, and the club secretary can block courts for matches. Swap tennis for meeting rooms, a shared van or allotment tools if you like. Booking looks simple, and it's where app builders show what they do and don't think about: rules, roles, and two people clicking at once.

**Build it in:** Lovable. **Time:** an evening. **Needs:** a Lovable account.

## Start in Plan mode

> Build a booking page for a tennis club with four courts, open 07:00 to 22:00. Members sign in and book a court for one hour, up to seven days ahead, with at most two bookings each at a time. Members can cancel their own bookings. The club secretary can block a court for a match or for repairs, and sees who has booked what.

Read the plan for the rules. Did it keep all four: opening hours, seven days ahead, two at a time, the secretary's blocks?

## Then, one change at a time

- "Show the week as a grid: courts across the top, hours down the side, my bookings in a different colour."
- "Send me an email when someone cancels a court I wanted." (See what it needs to send email.)
- "Members can book for a guest, who pays 5 pounds at the clubhouse."
- "Floodlit courts 3 and 4 can be booked until 22:00; courts 1 and 2 only until dusk."

## Watch for

- **Double bookings.** Open the page as two members in two browsers and book the same court and hour at the same moment. Then ask in Chat mode: "What stops two members booking the same court at the same time?" Is the answer in the database, or only on the page?
- **Who can see what.** Can a member see other members' names, emails or phone numbers? Should they?
- **The secretary.** How did it decide who the secretary is? Could any member make themselves one?

## Try this

1. Add the club's real rules, word for word, to the project's Instructions, and ask it to check every page against them.
2. Ask in Chat mode for a list of every rule the app enforces. Compare it with what you asked for.
3. Run the deep security scan, and fix what it finds one message at a time.
4. Add a waiting list: when a booked court is cancelled, the first member waiting gets it.
5. Sync to GitHub, open it in Cursor, and in Ask mode find exactly where the two-bookings limit is checked.

## Questions

For discussion. There are no right answers.

- The app enforces the rules you gave it. Who should be able to change those rules once it's live?
- Booking apps exist already. When is it worth building your own with a tool like this, and when isn't it?
- If a double booking does happen on a Saturday morning, who finds out first, and how?
