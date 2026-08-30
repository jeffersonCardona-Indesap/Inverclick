/*TRUNCATE TABLE country, prefix RESTART IDENTITY CASCADE;*/
UPDATE "country" AS c
SET "idPrefix" = p."id"
FROM "prefix" AS p
WHERE c."ISO" = p."ISO";