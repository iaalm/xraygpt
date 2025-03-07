X_RAY_DB_INIT_SCRIPT = """
PRAGMA user_version = 1;

CREATE TABLE string(id INTEGER, language TEXT, text TEXT);
CREATE TABLE source(id INTEGER, label INTEGER, url INTEGER, license_label INTEGER, license_url INTEGER, PRIMARY KEY(id));
CREATE TABLE entity(id INTEGER, label TEXT, loc_label INTEGER, type INTEGER, count INTEGER, has_info_card TINYINT, PRIMARY KEY(id));
CREATE TABLE entity_description(text TEXT, source_wildcard TEXT, source INTEGER, entity INTEGER, PRIMARY KEY(entity));
CREATE TABLE type(id INTEGER, label INTEGER, singular_label INTEGER, icon INTEGER, top_mentioned_entities TEXT, PRIMARY KEY(id));
CREATE TABLE entity_excerpt(entity INTEGER, excerpt INTEGER);
CREATE TABLE excerpt(id INTEGER, start INTEGER, length INTEGER, image TEXT, related_entities TEXT, goto INTEGER, PRIMARY KEY(id));
CREATE TABLE occurrence(entity INTEGER, start INTEGER, length INTEGER);
CREATE TABLE book_metadata(srl INTEGER, erl INTEGER, has_images TINYINT, has_excerpts TINYINT, show_spoilers_default TINYINT, num_people INTEGER, num_terms INTEGER, num_images INTEGER, preview_images TEXT);
CREATE INDEX idx_occurrence_start ON occurrence(start ASC);
CREATE INDEX idx_entity_excerpt ON entity_excerpt(entity ASC);
CREATE INDEX idx_entity_type ON entity(type ASC);

INSERT INTO book_metadata (srl, erl, has_images, has_excerpts, show_spoilers_default, num_people, num_terms, num_images, preview_images) VALUES(0, 9223372036854775807, 0, 0, 1, 0, 0, 0, "");
INSERT INTO entity (id, loc_label, has_info_card) VALUES(0, 1, 0);
INSERT INTO source (id, label, url) VALUES(0, 5, 20);
INSERT INTO source VALUES(1, 6, 21, 7, 8);
INSERT INTO string VALUES
( 0, "de", "Alle" ),
( 0, "en", "All" ),
( 0, "en-AU", "All" ),
( 0, "en-CA", "All" ),
( 0, "en-IN", "All" ),
( 0, "en-US", "All" ),
( 0, "es", "Todo" ),
( 0, "es-MX", "Todo" ),
( 0, "es-US", "Todo" ),
( 0, "fr", "Tout" ),
( 0, "fr-CA", "Tout" ),
( 0, "hi-IN", "सभी" ),
( 0, "it", "Tutto" ),
( 0, "ja", "すべて" ),
( 0, "nl", "Alles" ),
( 0, "pt-BR", "Todos" ),
( 0, "ru", "Все" ),
( 0, "zh-CN", "全部" ),
( 0, "zh-HK", "所有" ),
( 0, "zh-TW", "所有" ),
( 1, "de", "Buch" ),
( 1, "en", "Book" ),
( 1, "en-AU", "Book" ),
( 1, "en-CA", "Book" ),
( 1, "en-IN", "Book" ),
( 1, "en-US", "Book" ),
( 1, "es", "Libro" ),
( 1, "es-MX", "Libro" ),
( 1, "es-US", "Libro" ),
( 1, "fr", "Livre" ),
( 1, "fr-CA", "Livre" ),
( 1, "hi-IN", "किताब" ),
( 1, "it", "Libro" ),
( 1, "ja", "本" ),
( 1, "nl", "Boek" ),
( 1, "pt-BR", "Livro" ),
( 1, "ru", "Книга" ),
( 1, "zh-CN", "电子书" ),
( 1, "zh-HK", "書" ),
( 1, "zh-TW", "書" ),
( 2, "de", "Baidu Baike" ),
( 2, "en", "Baidu Baike" ),
( 2, "en-AU", "Baidu Baike" ),
( 2, "en-CA", "Baidu Baike" ),
( 2, "en-IN", "Baidu Baike" ),
( 2, "en-US", "Baidu Baike" ),
( 2, "es", "Baidu Baike" ),
( 2, "es-MX", "Baidu Baike" ),
( 2, "es-US", "Baidu Baike" ),
( 2, "fr", "Baidu Baike" ),
( 2, "fr-CA", "Baidu Baike" ),
( 2, "hi-IN", "Baidu Baike" ),
( 2, "it", "Baidu Baike" ),
( 2, "ja", "百度百科" ),
( 2, "nl", "Baidu Baike" ),
( 2, "pt-BR", "Baidu Baike" ),
( 2, "ru", "Baidu Baike" ),
( 2, "zh-CN", "百度百科" ),
( 2, "zh-HK", "百度百科" ),
( 2, "zh-TW", "百度百科" ),
( 3, "de", "Autor" ),
( 3, "en", "Author" ),
( 3, "en-AU", "Author" ),
( 3, "en-CA", "Author" ),
( 3, "en-IN", "Author" ),
( 3, "en-US", "Author" ),
( 3, "es", "Autor" ),
( 3, "es-MX", "Autor" ),
( 3, "es-US", "Autor" ),
( 3, "fr", "Auteur" ),
( 3, "fr-CA", "Auteur" ),
( 3, "hi-IN", "लेखक" ),
( 3, "it", "Autore" ),
( 3, "ja", "著者" ),
( 3, "nl", "Auteur" ),
( 3, "pt-BR", "Autor" ),
( 3, "ru", "Автор" ),
( 3, "zh-CN", "作者" ),
( 3, "zh-HK", "作者" ),
( 3, "zh-TW", "作者" ),
( 4, "de", "Fandom" ),
( 4, "en", "Fandom" ),
( 4, "en-AU", "Fandom" ),
( 4, "en-CA", "Fandom" ),
( 4, "en-IN", "Fandom" ),
( 4, "en-US", "Fandom" ),
( 4, "es", "Fandom" ),
( 4, "es-MX", "Fandom" ),
( 4, "es-US", "Fandom" ),
( 4, "fr", "Fandom" ),
( 4, "fr-CA", "Fandom" ),
( 4, "hi-IN", "Fandom" ),
( 4, "it", "Fandom" ),
( 4, "ja", "Fandom" ),
( 4, "nl", "Fandom" ),
( 4, "pt-BR", "Fandom" ),
( 4, "ru", "Fandom" ),
( 4, "zh-CN", "Fandom" ),
( 4, "zh-HK", "Fandom" ),
( 4, "zh-TW", "Fandom" ),
( 5, "de", "Kindle-Shop" ),
( 5, "en", "Kindle Store" ),
( 5, "en-AU", "Kindle Store" ),
( 5, "en-CA", "Kindle Store" ),
( 5, "en-IN", "Kindle Store" ),
( 5, "en-US", "Kindle Store" ),
( 5, "es", "Tienda Kindle" ),
( 5, "es-MX", "Tienda Kindle" ),
( 5, "es-US", "Tienda Kindle" ),
( 5, "fr", "Boutique Kindle" ),
( 5, "fr-CA", "Boutique Kindle" ),
( 5, "hi-IN", "Kindle स्टोर" ),
( 5, "it", "Kindle Store" ),
( 5, "ja", "Kindleストア" ),
( 5, "nl", "Kindle-winkel" ),
( 5, "pt-BR", "Loja Kindle" ),
( 5, "ru", "Магазин Kindle" ),
( 5, "zh-CN", "Kindle 商店" ),
( 5, "zh-HK", "Kindle 商店" ),
( 5, "zh-TW", "Kindle 商店" ),
( 6, "de", "Wikipedia" ),
( 6, "en", "Wikipedia" ),
( 6, "en-AU", "Wikipedia" ),
( 6, "en-CA", "Wikipedia" ),
( 6, "en-IN", "Wikipedia" ),
( 6, "en-US", "Wikipedia" ),
( 6, "es", "Wikipedia" ),
( 6, "es-MX", "Wikipedia" ),
( 6, "es-US", "Wikipedia" ),
( 6, "fr", "Wikipédia" ),
( 6, "fr-CA", "Wikipédia" ),
( 6, "hi-IN", "Wikipedia" ),
( 6, "it", "Wikipedia" ),
( 6, "ja", "Wikipedia" ),
( 6, "nl", "Wikipedia" ),
( 6, "pt-BR", "Wikipédia" ),
( 6, "ru", "Википедия" ),
( 6, "zh-CN", "维基百科" ),
( 6, "zh-HK", "維基百科" ),
( 6, "zh-TW", "維基百科" ),
( 7, "en", "Creative Commons Attribution Share-Alike license" ),
( 8, "en", "http://creativecommons.org/licenses/by-sa/3.0/legalcode" ),
( 1000, "de", "Wichtige Clips" ),
( 1000, "en", "Notable Clips" ),
( 1000, "en-AU", "Notable Clips" ),
( 1000, "en-CA", "Notable Clips" ),
( 1000, "en-IN", "Notable Clips" ),
( 1000, "en-US", "Notable Clips" ),
( 1000, "es", "Recortes destacados" ),
( 1000, "es-MX", "Recortes destacables" ),
( 1000, "es-US", "Recortes destacables" ),
( 1000, "fr", "Extraits importants" ),
( 1000, "fr-CA", "Extraits importants" ),
( 1000, "hi-IN", "चर्चित क्लिप" ),
( 1000, "it", "Ritagli rilevanti" ),
( 1000, "ja", "重要な抜粋" ),
( 1000, "nl", "Opvallende clips" ),
( 1000, "pt-BR", "Recortes notáveis" ),
( 1000, "ru", "Важные отрывки" ),
( 1000, "zh-CN", "选段" ),
( 1000, "zh-HK", "熱門片段" ),
( 1000, "zh-TW", "熱門片段" ),
( 1001, "de", "Wichtige Clips" ),
( 1001, "en", "Notable Clips" ),
( 1001, "en-AU", "Notable Clips" ),
( 1001, "en-CA", "Notable Clips" ),
( 1001, "en-IN", "Notable Clips" ),
( 1001, "en-US", "Notable Clips" ),
( 1001, "es", "Recortes destacados" ),
( 1001, "es-MX", "Recortes destacables" ),
( 1001, "es-US", "Recortes destacables" ),
( 1001, "fr", "Extraits importants" ),
( 1001, "fr-CA", "Extraits importants" ),
( 1001, "hi-IN", "चर्चित क्लिप" ),
( 1001, "it", "Ritagli rilevanti" ),
( 1001, "ja", "重要な抜粋" ),
( 1001, "nl", "Opvallende clips" ),
( 1001, "pt-BR", "Recortes notáveis" ),
( 1001, "ru", "Важные отрывки" ),
( 1001, "zh-CN", "选段" ),
( 1001, "zh-HK", "熱門片段" ),
( 1001, "zh-TW", "熱門片段" ),
( 9, "de", "Inhalt ist unangemessen" ),
( 9, "en", "Content is inappropriate" ),
( 9, "en-AU", "Content is inappropriate" ),
( 9, "en-CA", "Content is inappropriate" ),
( 9, "en-IN", "Content is inappropriate" ),
( 9, "en-US", "Content is inappropriate" ),
( 9, "es", "El contenido es inapropiado" ),
( 9, "es-MX", "El contenido es inapropiado" ),
( 9, "es-US", "El contenido es inapropiado" ),
( 9, "fr", "Le contenu est inapproprié" ),
( 9, "fr-CA", "Le contenu est inapproprié" ),
( 9, "hi-IN", "कॉन्टेंट आपत्तिजनक है" ),
( 9, "it", "Il contenuto è inappropriato" ),
( 9, "ja", "不適切なコンテンツ" ),
( 9, "nl", "Inhoud is ongepast" ),
( 9, "pt-BR", "O conteúdo é inadequado" ),
( 9, "ru", "Недопустимое содержимое" ),
( 9, "zh-CN", "内容不当" ),
( 9, "zh-HK", "內容不適當" ),
( 9, "zh-TW", "內容不適當" ),
( 10, "de", "Inhalt ist falsch" ),
( 10, "en", "Content is incorrect" ),
( 10, "en-AU", "Content is incorrect" ),
( 10, "en-CA", "Content is incorrect" ),
( 10, "en-IN", "Content is incorrect" ),
( 10, "en-US", "Content is incorrect" ),
( 10, "es", "El contenido es incorrecto" ),
( 10, "es-MX", "El contenido es incorrecto" ),
( 10, "es-US", "El contenido es incorrecto" ),
( 10, "fr", "Le contenu est incorrect" ),
( 10, "fr-CA", "Le contenu est incorrect" ),
( 10, "hi-IN", "कॉन्टेंट गलत है" ),
( 10, "it", "Il contenuto non è corretto" ),
( 10, "ja", "コンテンツが正しくありません" ),
( 10, "nl", "Inhoud is onjuist" ),
( 10, "pt-BR", "O conteúdo está incorreto" ),
( 10, "ru", "Неверное содержимое" ),
( 10, "zh-CN", "内容有误" ),
( 10, "zh-HK", "內容不正確" ),
( 10, "zh-TW", "內容不正確" ),
( 11, "de", "Inhalt benötigt mehr Details" ),
( 11, "en", "Content needs more detail" ),
( 11, "en-AU", "Content needs more detail" ),
( 11, "en-CA", "Content needs more detail" ),
( 11, "en-IN", "Content needs more detail" ),
( 11, "en-US", "Content needs more detail" ),
( 11, "es", "El contenido necesita más detalles" ),
( 11, "es-MX", "El contenido necesita más detalles" ),
( 11, "es-US", "El contenido necesita más detalles" ),
( 11, "fr", "Le contenu requiert plus de détails" ),
( 11, "fr-CA", "Le contenu requiert plus de détails" ),
( 11, "hi-IN", "कॉन्टेंट में और जानकारी की ज़रूरत है" ),
( 11, "it", "Il contenuto necessita di maggiori dettagli" ),
( 11, "ja", "コンテンツの詳細情報が不十分" ),
( 11, "nl", "Inhoud heeft meer details nodig" ),
( 11, "pt-BR", "O conteúdo precisa de mais detalhes" ),
( 11, "ru", "Требуется больше подробностей" ),
( 11, "zh-CN", "内容需要更多详情" ),
( 11, "zh-HK", "內容需要更多詳細資料" ),
( 11, "zh-TW", "內容需要更多詳細資料" ),
( 12, "de", "Etwas anderes..." ),
( 12, "en", "Something else..." ),
( 12, "en-AU", "Something else..." ),
( 12, "en-CA", "Something else..." ),
( 12, "en-IN", "Something else..." ),
( 12, "en-US", "Something else..." ),
( 12, "es", "Otra cosa..." ),
( 12, "es-MX", "Algo más..." ),
( 12, "es-US", "Algo más..." ),
( 12, "fr", "Autre..." ),
( 12, "fr-CA", "Autre chose..." ),
( 12, "hi-IN", "कुछ और..." ),
( 12, "it", "Qualcosa d'altro..." ),
( 12, "ja", "その他..." ),
( 12, "nl", "Iets anders…" ),
( 12, "pt-BR", "Outra coisa…" ),
( 12, "ru", "Другое…" ),
( 12, "zh-CN", "其他…" ),
( 12, "zh-HK", "其他..." ),
( 12, "zh-TW", "其他..." ),
( 13, "de", "Inhalt enthält Spoiler" ),
( 13, "en", "Content has spoilers" ),
( 13, "en-AU", "Content has spoilers" ),
( 13, "en-CA", "Content has spoilers" ),
( 13, "en-IN", "Content has spoilers" ),
( 13, "en-US", "Content has spoilers" ),
( 13, "es", "El contenido incluye detalles importantes sobre la trama" ),
( 13, "es-MX", "El contenido incluye detalles importantes sobre la trama" ),
( 13, "es-US", "El contenido incluye detalles importantes sobre la trama" ),
( 13, "fr", "Le contenu révèle une partie de l'intrigue" ),
( 13, "fr-CA", "Le contenu révèle une partie de l'intrigue" ),
( 13, "hi-IN", "कॉन्टेंट में खराबी पैदा करने वाली चीज़ें हैं" ),
( 13, "it", "Il contenuto include spoiler" ),
( 13, "ja", "コンテンツにネタバレが含まれています" ),
( 13, "nl", "Inhoud bevat spoilers" ),
( 13, "pt-BR", "O conteúdo possui spoilers" ),
( 13, "ru", "Спойлеры в содержимом" ),
( 13, "zh-CN", "内容包含剧透" ),
( 13, "zh-HK", "內容包含搶先透露情節" ),
( 13, "zh-TW", "內容包含搶先透露情節" ),
( 14, "de", "Personen" ),
( 14, "en", "People" ),
( 14, "en-AU", "People" ),
( 14, "en-CA", "People" ),
( 14, "en-IN", "People" ),
( 14, "en-US", "People" ),
( 14, "es", "Gente" ),
( 14, "es-MX", "Personas" ),
( 14, "es-US", "Personas" ),
( 14, "fr", "Personnes" ),
( 14, "fr-CA", "Personnes" ),
( 14, "hi-IN", "लोग" ),
( 14, "it", "Persone" ),
( 14, "ja", "人物" ),
( 14, "nl", "Mensen" ),
( 14, "pt-BR", "Pessoas" ),
( 14, "ru", "Люди" ),
( 14, "zh-CN", "人物" ),
( 14, "zh-HK", "人" ),
( 14, "zh-TW", "人" ),
( 15, "de", "Person" ),
( 15, "en", "Person" ),
( 15, "en-AU", "Person" ),
( 15, "en-CA", "Person" ),
( 15, "en-IN", "Person" ),
( 15, "en-US", "Person" ),
( 15, "es", "Persona" ),
( 15, "es-MX", "Persona" ),
( 15, "es-US", "Persona" ),
( 15, "fr", "Personne" ),
( 15, "fr-CA", "Personne" ),
( 15, "hi-IN", "व्यक्ति" ),
( 15, "it", "Persona" ),
( 15, "ja", "人物" ),
( 15, "nl", "Persoon" ),
( 15, "pt-BR", "Pessoa" ),
( 15, "ru", "Человек" ),
( 15, "zh-CN", "人物" ),
( 15, "zh-HK", "人" ),
( 15, "zh-TW", "人" ),
( 16, "de", "Begriffe" ),
( 16, "en", "Terms" ),
( 16, "en-AU", "Terms" ),
( 16, "en-CA", "Terms" ),
( 16, "en-IN", "Terms" ),
( 16, "en-US", "Terms" ),
( 16, "es", "Términos" ),
( 16, "es-MX", "Términos" ),
( 16, "es-US", "Términos" ),
( 16, "fr", "Termes" ),
( 16, "fr-CA", "Termes" ),
( 16, "hi-IN", "शर्तें" ),
( 16, "it", "Termini" ),
( 16, "ja", "トピック" ),
( 16, "nl", "Termen" ),
( 16, "pt-BR", "Termos" ),
( 16, "ru", "Термины" ),
( 16, "zh-CN", "术语" ),
( 16, "zh-HK", "字詞" ),
( 16, "zh-TW", "字詞" ),
( 17, "de", "Begriff" ),
( 17, "en", "Term" ),
( 17, "en-AU", "Term" ),
( 17, "en-CA", "Term" ),
( 17, "en-IN", "Term" ),
( 17, "en-US", "Term" ),
( 17, "es", "Término" ),
( 17, "es-MX", "Término" ),
( 17, "es-US", "Término" ),
( 17, "fr", "Terme" ),
( 17, "fr-CA", "Terme" ),
( 17, "hi-IN", "शर्त" ),
( 17, "it", "Termine" ),
( 17, "ja", "トピック" ),
( 17, "nl", "Term" ),
( 17, "pt-BR", "Termo" ),
( 17, "ru", "Термин" ),
( 17, "zh-CN", "术语" ),
( 17, "zh-HK", "字詞" ),
( 17, "zh-TW", "字詞" ),
( 18, "de", "Themen" ),
( 18, "en", "Themes" ),
( 18, "en-AU", "Themes" ),
( 18, "en-CA", "Themes" ),
( 18, "en-IN", "Themes" ),
( 18, "en-US", "Themes" ),
( 18, "es", "Temas" ),
( 18, "es-MX", "Temas" ),
( 18, "es-US", "Temas" ),
( 18, "fr", "Thèmes" ),
( 18, "fr-CA", "Thèmes" ),
( 18, "hi-IN", "थीम" ),
( 18, "it", "Temi" ),
( 18, "ja", "テーマ" ),
( 18, "nl", "Thema's" ),
( 18, "pt-BR", "Tema" ),
( 18, "ru", "Темы" ),
( 18, "zh-CN", "主题" ),
( 18, "zh-HK", "主題" ),
( 18, "zh-TW", "主題" ),
( 19, "de", "Thema" ),
( 19, "en", "Theme" ),
( 19, "en-AU", "Theme" ),
( 19, "en-CA", "Theme" ),
( 19, "en-IN", "Theme" ),
( 19, "en-US", "Theme" ),
( 19, "es", "Tema" ),
( 19, "es-MX", "Tema" ),
( 19, "es-US", "Tema" ),
( 19, "fr", "Thème" ),
( 19, "fr-CA", "Thème" ),
( 19, "hi-IN", "थीम" ),
( 19, "it", "Tema" ),
( 19, "ja", "テーマ" ),
( 19, "nl", "Thema" ),
( 19, "pt-BR", "Tema" ),
( 19, "ru", "Тема" ),
( 19, "zh-CN", "主题" ),
( 19, "zh-HK", "主題" ),
( 19, "zh-TW", "主題" ),
( 20, "en", "store://%s" );
"""
