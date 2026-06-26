-- Run this in Supabase SQL editor

create extension if not exists vector;

create table users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  created_at timestamptz default now()
);

create table interviews (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id),
  state text not null default 'PREPARED',
  role_profile jsonb,
  blueprint jsonb,
  concept_graph jsonb default '{}'::jsonb,
  time_remaining_seconds int default 2400,
  created_at timestamptz default now(),
  completed_at timestamptz
);

create table uploaded_files (
  id uuid primary key default gen_random_uuid(),
  interview_id uuid references interviews(id),
  user_id uuid references users(id),
  file_type text, -- resume | job_description
  storage_path text,
  parsed_json jsonb,
  created_at timestamptz default now()
);

create table extracted_skills (
  id uuid primary key default gen_random_uuid(),
  file_id uuid references uploaded_files(id),
  label text not null,
  category text,
  confidence float,
  source_span text,
  embedding vector(768)  -- pgvector
);

create table skill_matches (
  id uuid primary key default gen_random_uuid(),
  interview_id uuid references interviews(id),
  match_score float,
  matches jsonb,
  gaps jsonb,
  created_at timestamptz default now()
);

create table interview_questions (
  id uuid primary key default gen_random_uuid(),
  interview_id uuid references interviews(id),
  sequence_number int,
  topic text,
  subtopic text,
  difficulty int,
  question text,
  expected_concepts jsonb,
  purpose text,
  asked_at timestamptz default now()
);

create table transcript_segments (
  id uuid primary key default gen_random_uuid(),
  interview_id uuid references interviews(id),
  question_id uuid references interview_questions(id),
  segment_type text, -- partial | final
  text text,
  created_at timestamptz default now()
);

create table answer_evaluations (
  id uuid primary key default gen_random_uuid(),
  interview_id uuid references interviews(id),
  question_id uuid references interview_questions(id),
  correctness float,
  communication float,
  confidence float,
  completeness float,
  keyword_coverage float,
  strengths jsonb,
  misconceptions jsonb,
  missing_concepts jsonb,
  rationale text,
  created_at timestamptz default now()
);

create table reports (
  id uuid primary key default gen_random_uuid(),
  interview_id uuid references interviews(id) unique,
  overall_score float,
  dimension_scores jsonb,
  weak_concepts jsonb,
  roadmap jsonb,
  hiring_readiness text,
  created_at timestamptz default now()
);

-- Row Level Security
alter table interviews enable row level security;
create policy "users own interviews" on interviews using (auth.uid() = user_id);
