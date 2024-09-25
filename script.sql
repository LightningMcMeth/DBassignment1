USE assignment1;

CREATE TABLE cheeseburgers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30),
    type VARCHAR(20)
);

INSERT INTO cheeseburgers (name, type) values
('Big burger slam', 'double beef'),
('Downtown whopper', 'chicken'),
('Tripple delight deluxe', 'tripple beef'),
('Ronalds delightful surprise', 'egg and chicken');

UPDATE cheeseburgers SET type = 'double beef' WHERE name = 'Big burger slam'