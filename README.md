## Database

**Database:** PostgreSQL (hosted on Supabase)
**ORM:** SQLAlchemy

### Why PostgreSQL
PostgreSQL was chosen for its strong relational integrity, native support for foreign keys, 
and reliability for structured data like users, conversations, and messages. Supabase was 
used as the hosting provider since it offers a free managed Postgres instance with an 
easy-to-use dashboard for inspecting tables directly.

### Schema Diagram
![Schema Diagram](./W5_SchemaDiagram_[InternID].png)

**Entities:**
- **Task** — standalone to-do items (id, title, done, created_at)
- **User** — app users (id, name, email, created_at)
- **Conversation** — belongs to a User (one-to-many)
- **Message** — belongs to a Conversation (one-to-many); `is_bot` distinguishes chatbot replies from user messages

### Set up the database
1. Create a free PostgreSQL database (e.g. via [Supabase](https://supabase.com) or [Neon](https://neon.tech))
2. Copy `.env.example` to `.env`:
```bash
   cp backend/.env.example backend/.env
```
3. Fill in your real `DATABASE_URL` in `.env`:
