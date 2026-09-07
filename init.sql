CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE bookmarks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    page_id INTEGER NOT NULL REFERENCES pages(id) ON DELETE CASCADE
);

-- Default pages
INSERT INTO pages (name) VALUES ('University');
INSERT INTO pages (name) VALUES ('Personal');
INSERT INTO pages (name) VALUES ('Recipes');

-- Sample bookmarks in the default page (page_id = 1)
INSERT INTO bookmarks (title, url, page_id) VALUES
('Otago', 'https://otago.ac.nz', 1),
('Docker Docs', 'https://docs.docker.com', 1),
('Otago COSC349', 'https://cs.otago.ac.nz/cosc349', 1);

-- Sample bookmarks in the Personal page (page_id = 2)
INSERT INTO bookmarks (title, url, page_id) VALUES
('GitHub', 'https://github.com', 2),
('Stack Overflow', 'https://stackoverflow.com', 2);

-- Sample bookmarks in the Recipes page (page_id = 3)
INSERT INTO bookmarks (title, url, page_id) VALUES
('AllRecipes', 'https://allrecipes.com', 3),
('Food Network', 'https://foodnetwork.com', 3);