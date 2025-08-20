CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE supplements (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    symptoms JSONB          
);

INSERT INTO supplements (name, description, symptoms) VALUES
('Vitamin D', 'Supports bone health and immune function', '{"fatigue": true, "muscle_weakness": true, "headache": false}'),
('Vitamin C', 'Supports immune system and skin health', '{"fatigue": true, "headache": false, "muscle_weakness": false}'),
('Magnesium', 'Helps muscle function and energy production', '{"fatigue": true, "muscle_weakness": true, "headache": true}'),
('Omega-3', 'Supports brain and heart health', '{"fatigue": false, "headache": false, "muscle_weakness": false}'),
('Probiotics', 'Supports digestive health and immunity', '{"fatigue": false, "headache": false, "muscle_weakness": false}'),
('Zinc', 'Supports immune system and wound healing', '{"fatigue": true, "headache": false, "muscle_weakness": false}'),
('Calcium', 'Essential for bone and teeth strength', '{"fatigue": false, "muscle_weakness": true, "headache": false}'),
('Iron', 'Supports red blood cells and oxygen transport', '{"fatigue": true, "headache": true, "muscle_weakness": true}'),
('B-Complex Vitamins', 'Supports energy metabolism and brain function', '{"fatigue": true, "headache": true, "muscle_weakness": false}'),
('Vitamin B12', 'Important for nerve function and blood formation', '{"fatigue": true, "headache": true, "muscle_weakness": true}'),
('Folic Acid', 'Supports cell growth and metabolism', '{"fatigue": true, "headache": false, "muscle_weakness": false}'),
('Coenzyme Q10', 'Supports energy production and heart health', '{"fatigue": true, "headache": false, "muscle_weakness": true}'),
('Turmeric', 'Anti-inflammatory and antioxidant support', '{"fatigue": false, "headache": true, "muscle_weakness": false}'),
('Ashwagandha', 'Helps reduce stress and fatigue', '{"fatigue": true, "headache": false, "muscle_weakness": false}'),
('Melatonin', 'Supports sleep regulation', '{"fatigue": true, "headache": false, "muscle_weakness": false}'),
('Collagen', 'Supports skin, hair, nails, and joints', '{"fatigue": false, "headache": false, "muscle_weakness": true}'),
('L-Theanine', 'Promotes relaxation and focus', '{"fatigue": true, "headache": false, "muscle_weakness": false}'),
('Glucosamine', 'Supports joint health', '{"fatigue": false, "headache": false, "muscle_weakness": true}'),
('Choline', 'Supports brain health and liver function', '{"fatigue": true, "headache": false, "muscle_weakness": false}'),
('Calcium Magnesium Zinc', 'Supports bone health and muscle function', '{"fatigue": true, "muscle_weakness": true, "headache": false}');
