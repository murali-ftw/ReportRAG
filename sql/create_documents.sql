CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS reports(
    "Uuid" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "CompanyName" TEXT NOT NULL,
    "ReportType" TEXT NOT NULL,
    "DownloadURL" TEXT,
    "Path" TEXT NOT NULL,
    "DocumentYear" INTEGER NOT NULL,
    CONSTRAINT documents_company_report_year_unique UNIQUE (
        "CompanyName",
        "ReportType",
        "DocumentYear"
    )
);

INSERT INTO reports (
    "CompanyName",
    "ReportType",
    "DownloadURL",
    "Path",
    "DocumentYear"
) VALUES
    ('Walmart', 'Annual Report', NULL, '/Users/muralik/Documents/Programs/ReportRAG/reports/Walmart.pdf', 2025),
    ('Microsoft', 'Annual Report', NULL, '/Users/muralik/Documents/Programs/ReportRAG/reports/Microsoft.pdf', 2025),
    ('Aramco', 'Annual Report', NULL, '/Users/muralik/Documents/Programs/ReportRAG/reports/Aramco.pdf', 2025),
    ('JPMorgan', 'Annual Report', NULL, '/Users/muralik/Documents/Programs/ReportRAG/reports/JPMorgan.pdf', 2025)
ON CONFLICT ("CompanyName", "ReportType", "DocumentYear") DO UPDATE SET
    "DownloadURL" = EXCLUDED."DownloadURL",
    "Path" = EXCLUDED."Path";
