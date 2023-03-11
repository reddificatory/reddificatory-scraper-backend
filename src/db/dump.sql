CREATE TABLE IF NOT EXISTS submissions (
    "submission_id" VARCHAR ( 16 ) UNIQUE NOT NULL PRIMARY KEY,
    "subreddit" TEXT NOT NULL,
    "scraped" BOOLEAN DEFAULT FALSE,
    "used" BOOLEAN DEFAULT FALSE,
    "created_at" TIMESTAMP NOT NULL DEFAULT (current_timestamp),
    "updated_at" TIMESTAMP NOT NULL DEFAULT (current_timestamp)
);

CREATE TABLE IF NOT EXISTS comments (
    "comment_id" VARCHAR ( 16 ) UNIQUE NOT NULL PRIMARY KEY,
    "submission_id" VARCHAR ( 16 ) NOT NULL,
    "length" INTEGER NOT NULL,
    "used" BOOLEAN DEFAULT FALSE,
    "created_at" TIMESTAMP NOT NULL DEFAULT (current_timestamp),
    "updated_at" TIMESTAMP NOT NULL DEFAULT (current_timestamp),
    CONSTRAINT fk_submission_id FOREIGN KEY (submission_id) REFERENCES submissions(submission_id)
);