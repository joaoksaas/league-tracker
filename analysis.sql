-- KDA médio e quantidade de vitórias por Campeão
SELECT champion, AVG(kda), count(win)
FROM tb_match_stats
WHERE game_mode = "CLASSIC"
GROUP BY champion
ORDER BY AVG(kda) DESC;

SELECT *
FROM tb_match_stats
WHERE kda > 10.0;


-- Winrate médio e KDA médio por Campeão
SELECT
    champion,
    count(*) as total_jogos,
    sum(win) as qte_vitorias,
    round(AVG(win)*100, 1) as win_rate,
    round(AVG(kda), 2) as kda_medio
FROM tb_match_stats
WHERE game_mode = "CLASSIC"
GROUP BY champion
HAVING total_jogos >= 2
ORDER BY win_rate DESC;


-- Power Spike médio de ouro e dano por Campeão
SELECT 
    champion, 
    AVG(damage_dealt) as dano_medio, 
    AVG(gold_per_min) as gold_medio, 
    count(*) as total_jogos
FROM tb_match_stats
WHERE game_mode = "CLASSIC"
GROUP BY champion
HAVING total_jogos >= 2
ORDER BY gold_medio DESC

-- Partidas outliers - top 5 partidas com o maior dano 
SELECT 
    champion,
    win,
    kda,
    damage_dealt,
    vision_score,
    date
FROM tb_match_stats
WHERE game_mode = "CLASSIC"
ORDER BY damage_dealt DESC
LIMIT 5;

-- Impacto do score de visão e first blood na vitória
SELECT 
    win,
    count(*) as total_partidas,
    round(AVG(vision_score)*100, 2) as media_visao,
    round(AVG(time_ccing)*100, 2) as media_cc,
    sum(first_blood) as total_fb
FROM tb_match_stats
WHERE game_mode = "CLASSIC"
GROUP BY win