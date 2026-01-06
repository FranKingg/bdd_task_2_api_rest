-- Initial data for the Library API (PostgreSQL / SQLite compatible)

INSERT INTO categories (id, name, description, created_at, updated_at) VALUES
(1, 'Ficción', 'Narrativa y novelas', '2025-11-20T00:01:00+00:00', '2025-11-20T00:01:00+00:00'),
(2, 'No ficción', 'Ensayos y divulgación', '2025-11-20T00:02:00+00:00', '2025-11-20T00:02:00+00:00'),
(3, 'Ciencia', 'Ciencia y tecnología', '2025-11-20T00:03:00+00:00', '2025-11-20T00:03:00+00:00'),
(4, 'Historia', 'Historia universal', '2025-11-20T00:04:00+00:00', '2025-11-20T00:04:00+00:00'),
(5, 'Fantasía', 'Mundos fantásticos', '2025-11-20T00:05:00+00:00', '2025-11-20T00:05:00+00:00');

INSERT INTO users (id, username, fullname, password, email, phone, address, is_active, created_at, updated_at) VALUES
(1, 'user1', 'Usuario Uno', '$argon2id$v=19$m=65536,t=3,p=4$PTAD4R7nmkWfvakl2psGAg$XvzzJOCvVRsmLnTzXtySqrds5bt1T5iNRbmViWO4yPE', 'user1@example.com', '+56911111111', 'Punta Arenas', TRUE, '2025-11-20T01:41:00+00:00', '2025-11-20T01:41:00+00:00'),
(2, 'user2', 'Usuario Dos', '$argon2id$v=19$m=65536,t=3,p=4$BVsI6E5+bR3g4zHH4OwuCA$WAmGows+EiFS12fdMA+Er6DC+AoN4RO5gDI9Lrgs/Cw', 'user2@example.com', NULL, NULL, TRUE, '2025-11-20T01:42:00+00:00', '2025-11-20T01:42:00+00:00'),
(3, 'user3', 'Usuario Tres', '$argon2id$v=19$m=65536,t=3,p=4$0MzsHoJYc6U+yQc+xMylOA$LgpdWyDZstbYJ7GL2VfeeZPRTUU/hRplPNOgmEQNDoA', 'user3@example.com', '+56933333333', 'Puerto Natales', TRUE, '2025-11-20T01:43:00+00:00', '2025-11-20T01:43:00+00:00'),
(4, 'user4', 'Usuario Cuatro', '$argon2id$v=19$m=65536,t=3,p=4$MA/xp2gh/IfZS3wCCbAeyw$VH1dkLTF6t5p0msB5QPL8y9UCCB12t33RX6J3JzQPUw', 'user4@example.com', NULL, 'Santiago', FALSE, '2025-11-20T01:44:00+00:00', '2025-11-20T01:44:00+00:00'),
(5, 'user5', 'Usuario Cinco', '$argon2id$v=19$m=65536,t=3,p=4$FgEIVPec9p0lo97UCbpEMw$oFAUF6NF1Jwlm8+gMYE9tZYTfDAd5q/qcyqO7iRzTxA', 'user5@example.com', '+56955555555', NULL, TRUE, '2025-11-20T01:45:00+00:00', '2025-11-20T01:45:00+00:00');

INSERT INTO books (id, title, author, isbn, pages, published_year, stock, description, language, publisher, created_at, updated_at) VALUES
(1, 'Libro 1', 'Autor 1', 'ISBN-BD2-2025-1001', 110, 2001, 3, 'Descripción del libro 1', 'en', 'Editorial 2', '2025-11-20T03:21:00+00:00', '2025-11-20T03:21:00+00:00'),
(2, 'Libro 2', 'Autor 2', 'ISBN-BD2-2025-1002', 120, 2002, 3, 'Descripción del libro 2', 'fr', 'Editorial 3', '2025-11-20T03:22:00+00:00', '2025-11-20T03:22:00+00:00'),
(3, 'Libro 3', 'Autor 3', 'ISBN-BD2-2025-1003', 130, 2003, 1, 'Descripción del libro 3', 'es', 'Editorial 1', '2025-11-20T03:23:00+00:00', '2025-11-20T03:23:00+00:00'),
(4, 'Libro 4', 'Autor 4', 'ISBN-BD2-2025-1004', 140, 2004, 3, 'Descripción del libro 4', 'en', 'Editorial 2', '2025-11-20T03:24:00+00:00', '2025-11-20T03:24:00+00:00'),
(5, 'Libro 5', 'Autor 1', 'ISBN-BD2-2025-1005', 150, 2005, 3, 'Descripción del libro 5', 'fr', 'Editorial 3', '2025-11-20T03:25:00+00:00', '2025-11-20T03:25:00+00:00'),
(6, 'Libro 6', 'Autor 2', 'ISBN-BD2-2025-1006', 160, 2006, 1, 'Descripción del libro 6', 'es', 'Editorial 1', '2025-11-20T03:26:00+00:00', '2025-11-20T03:26:00+00:00'),
(7, 'Libro 7', 'Autor 3', 'ISBN-BD2-2025-1007', 170, 2007, 3, 'Descripción del libro 7', 'en', 'Editorial 2', '2025-11-20T03:27:00+00:00', '2025-11-20T03:27:00+00:00'),
(8, 'Libro 8', 'Autor 4', 'ISBN-BD2-2025-1008', 180, 2008, 3, 'Descripción del libro 8', 'fr', 'Editorial 3', '2025-11-20T03:28:00+00:00', '2025-11-20T03:28:00+00:00'),
(9, 'Libro 9', 'Autor 1', 'ISBN-BD2-2025-1009', 190, 2009, 1, 'Descripción del libro 9', 'es', 'Editorial 1', '2025-11-20T03:29:00+00:00', '2025-11-20T03:29:00+00:00'),
(10, 'Libro 10', 'Autor 2', 'ISBN-BD2-2025-1010', 200, 2010, 3, 'Descripción del libro 10', 'en', 'Editorial 2', '2025-11-20T03:30:00+00:00', '2025-11-20T03:30:00+00:00');

INSERT INTO book_categories (book_id, category_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 1),
(7, 2),
(8, 3),
(9, 4),
(10, 5);

INSERT INTO loans (id, loan_dt, due_date, return_dt, fine_amount, status, user_id, book_id, created_at, updated_at) VALUES
(1, '2025-11-25', '2025-12-09', NULL, NULL, 'ACTIVE', 1, 1, '2025-11-20T05:01:00+00:00', '2025-11-20T05:01:00+00:00'),
(2, '2025-11-10', '2025-11-24', NULL, NULL, 'OVERDUE', 2, 2, '2025-11-20T05:02:00+00:00', '2025-11-20T05:02:00+00:00'),
(3, '2025-11-01', '2025-11-15', '2025-11-10', NULL, 'RETURNED', 3, 3, '2025-11-20T05:03:00+00:00', '2025-11-20T05:03:00+00:00'),
(4, '2025-11-01', '2025-11-15', '2025-11-20', 25000, 'RETURNED', 4, 4, '2025-11-20T05:04:00+00:00', '2025-11-20T05:04:00+00:00'),
(5, '2025-11-28', '2025-12-12', NULL, NULL, 'ACTIVE', 5, 5, '2025-11-20T05:05:00+00:00', '2025-11-20T05:05:00+00:00'),
(6, '2025-10-20', '2025-11-03', NULL, NULL, 'OVERDUE', 1, 6, '2025-11-20T05:06:00+00:00', '2025-11-20T05:06:00+00:00'),
(7, '2025-11-15', '2025-11-29', '2025-11-18', NULL, 'RETURNED', 2, 7, '2025-11-20T05:07:00+00:00', '2025-11-20T05:07:00+00:00'),
(8, '2025-11-05', '2025-11-19', NULL, NULL, 'OVERDUE', 3, 8, '2025-11-20T05:08:00+00:00', '2025-11-20T05:08:00+00:00');

INSERT INTO reviews (id, rating, comment, review_date, user_id, book_id, created_at, updated_at) VALUES
(1, 5, 'Comentario 1', '2025-11-21', 1, 1, '2025-11-20T06:41:00+00:00', '2025-11-20T06:41:00+00:00'),
(2, 5, 'Comentario 2', '2025-11-22', 2, 1, '2025-11-20T06:42:00+00:00', '2025-11-20T06:42:00+00:00'),
(3, 5, 'Comentario 3', '2025-11-23', 3, 2, '2025-11-20T06:43:00+00:00', '2025-11-20T06:43:00+00:00'),
(4, 2, 'Comentario 4', '2025-11-24', 4, 2, '2025-11-20T06:44:00+00:00', '2025-11-20T06:44:00+00:00'),
(5, 5, 'Comentario 5', '2025-11-25', 5, 3, '2025-11-20T06:45:00+00:00', '2025-11-20T06:45:00+00:00'),
(6, 5, 'Comentario 6', '2025-11-26', 1, 3, '2025-11-20T06:46:00+00:00', '2025-11-20T06:46:00+00:00'),
(7, 1, 'Comentario 7', '2025-11-27', 2, 4, '2025-11-20T06:47:00+00:00', '2025-11-20T06:47:00+00:00'),
(8, 2, 'Comentario 8', '2025-11-28', 3, 4, '2025-11-20T06:48:00+00:00', '2025-11-20T06:48:00+00:00'),
(9, 5, 'Comentario 9', '2025-11-29', 4, 5, '2025-11-20T06:49:00+00:00', '2025-11-20T06:49:00+00:00'),
(10, 5, 'Comentario 10', '2025-11-20', 5, 5, '2025-11-20T06:50:00+00:00', '2025-11-20T06:50:00+00:00'),
(11, 5, 'Comentario 11', '2025-11-21', 1, 6, '2025-11-20T06:51:00+00:00', '2025-11-20T06:51:00+00:00'),
(12, 2, 'Comentario 12', '2025-11-22', 2, 6, '2025-11-20T06:52:00+00:00', '2025-11-20T06:52:00+00:00'),
(13, 5, 'Comentario 13', '2025-11-23', 3, 7, '2025-11-20T06:53:00+00:00', '2025-11-20T06:53:00+00:00'),
(14, 1, 'Comentario 14', '2025-11-24', 4, 7, '2025-11-20T06:54:00+00:00', '2025-11-20T06:54:00+00:00'),
(15, 5, 'Comentario 15', '2025-11-25', 5, 8, '2025-11-20T06:55:00+00:00', '2025-11-20T06:55:00+00:00');
