SELECT DISTINCT p.name
FROM people p
JOIN stars s ON p.id = s.person_id
JOIN stars kb_s ON s.movie_id = kb_s.movie_id
JOIN people kb ON kb_s.person_id = kb.id
WHERE kb.name = 'Kevin Bacon'
  AND kb.birth = 1958
  AND p.name != 'Kevin Bacon';
