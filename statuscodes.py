#!/bin/python
# coding: utf-8

# Source: http://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
statuscodes = [
    (100, "Continue"),
    (101, "Switching Protocol"),
    (102, "Processing"),
    (200, "OK"),
    (201, "Created"),
    (202, "Accepted"),
    (203, "Non-Authoritative Information"),
    (204, "No Content"),
    (205, "Reset Content"),
    (206, "Partial Content"),
    (207, "Multi-Status"),
    (208, "Already Reported"),
    (226, "IM Used"),
    (300, "Multiple Choices"),
    (301, "Moved Permanently"),
    (302, "Found"),
    (303, "See Other"),
    (304, "Not Modified"),
    (305, "Use Proxy"),
    (307, "Temporary Redirect"),
    (308, "Permanent Redirect"),
    (400, "Bad Request"),
    (401, "Unauthorized"),
    (402, "Payment Required"),
    (403, "Forbidden"),
    (404, "Not Found"),
    (405, "Method Not Allowed"),
    (406, "Not Acceptable"),
    (407, "Proxy Authentication Required"),
    (408, "Request Timeout"),
    (409, "Conflict"),
    (410, "Gone"),
    (411, "Length Required"),
    (412, "Precondition Failed"),
    (413, "Payload Too Large"),
    (414, "URI Too Long"),
    (415, "Unsupported Media Type"),
    (416, "Range Not Satisfiable"),
    (417, "Expectation Failed"),
    (422, "Unprocessable Entity"),
    (423, "Locked"),
    (424, "Failed Dependency"),
    (426, "Upgrade Required"),
    (428, "Precondition Required"),
    (429, "Too Many Requests"),
    (431, "Request Header Fields Too Large"),
    (500, "Internal Server Error"),
    (501, "Not Implemented"),
    (502, "Bad Gateway"),
    (503, "Service Unavailable"),
    (504, "Gateway Timeout"),
    (505, "HTTP Version Not Supported"),
    (506, "Variant Also Negotiates"),
    (507, "Insufficient Storage"),
    (508, "Loop Detected"),
    (510, "Not Extended"),
    (511, "Network Authentication Required"),

    (103, "Unassigned"),
    (104, "Unassigned"),
    (105, "Unassigned"),
    (106, "Unassigned"),
    (107, "Unassigned"),
    (108, "Unassigned"),
    (109, "Unassigned"),
    (110, "Unassigned"),
    (111, "Unassigned"),
    (112, "Unassigned"),
    (113, "Unassigned"),
    (114, "Unassigned"),
    (115, "Unassigned"),
    (116, "Unassigned"),
    (117, "Unassigned"),
    (118, "Unassigned"),
    (119, "Unassigned"),
    (120, "Unassigned"),
    (121, "Unassigned"),
    (122, "Unassigned"),
    (123, "Unassigned"),
    (124, "Unassigned"),
    (125, "Unassigned"),
    (126, "Unassigned"),
    (127, "Unassigned"),
    (128, "Unassigned"),
    (129, "Unassigned"),
    (130, "Unassigned"),
    (131, "Unassigned"),
    (132, "Unassigned"),
    (133, "Unassigned"),
    (134, "Unassigned"),
    (135, "Unassigned"),
    (136, "Unassigned"),
    (137, "Unassigned"),
    (138, "Unassigned"),
    (139, "Unassigned"),
    (140, "Unassigned"),
    (141, "Unassigned"),
    (142, "Unassigned"),
    (143, "Unassigned"),
    (144, "Unassigned"),
    (145, "Unassigned"),
    (146, "Unassigned"),
    (147, "Unassigned"),
    (148, "Unassigned"),
    (149, "Unassigned"),
    (150, "Unassigned"),
    (151, "Unassigned"),
    (152, "Unassigned"),
    (153, "Unassigned"),
    (154, "Unassigned"),
    (155, "Unassigned"),
    (156, "Unassigned"),
    (157, "Unassigned"),
    (158, "Unassigned"),
    (159, "Unassigned"),
    (160, "Unassigned"),
    (161, "Unassigned"),
    (162, "Unassigned"),
    (163, "Unassigned"),
    (164, "Unassigned"),
    (165, "Unassigned"),
    (166, "Unassigned"),
    (167, "Unassigned"),
    (168, "Unassigned"),
    (169, "Unassigned"),
    (170, "Unassigned"),
    (171, "Unassigned"),
    (172, "Unassigned"),
    (173, "Unassigned"),
    (174, "Unassigned"),
    (175, "Unassigned"),
    (176, "Unassigned"),
    (177, "Unassigned"),
    (178, "Unassigned"),
    (179, "Unassigned"),
    (180, "Unassigned"),
    (181, "Unassigned"),
    (182, "Unassigned"),
    (183, "Unassigned"),
    (184, "Unassigned"),
    (185, "Unassigned"),
    (186, "Unassigned"),
    (187, "Unassigned"),
    (188, "Unassigned"),
    (189, "Unassigned"),
    (190, "Unassigned"),
    (191, "Unassigned"),
    (192, "Unassigned"),
    (193, "Unassigned"),
    (194, "Unassigned"),
    (195, "Unassigned"),
    (196, "Unassigned"),
    (197, "Unassigned"),
    (198, "Unassigned"),
    (199, "Unassigned"),
    (209, "Unassigned"),
    (210, "Unassigned"),
    (211, "Unassigned"),
    (212, "Unassigned"),
    (213, "Unassigned"),
    (214, "Unassigned"),
    (215, "Unassigned"),
    (216, "Unassigned"),
    (217, "Unassigned"),
    (218, "Unassigned"),
    (219, "Unassigned"),
    (220, "Unassigned"),
    (221, "Unassigned"),
    (222, "Unassigned"),
    (223, "Unassigned"),
    (224, "Unassigned"),
    (225, "Unassigned"),

    (227, "Unassigned"),
    (228, "Unassigned"),
    (229, "Unassigned"),
    (230, "Unassigned"),
    (231, "Unassigned"),
    (232, "Unassigned"),
    (233, "Unassigned"),
    (234, "Unassigned"),
    (235, "Unassigned"),
    (236, "Unassigned"),
    (237, "Unassigned"),
    (238, "Unassigned"),
    (239, "Unassigned"),
    (240, "Unassigned"),
    (241, "Unassigned"),
    (242, "Unassigned"),
    (243, "Unassigned"),
    (244, "Unassigned"),
    (245, "Unassigned"),
    (246, "Unassigned"),
    (247, "Unassigned"),
    (248, "Unassigned"),
    (249, "Unassigned"),
    (250, "Unassigned"),
    (251, "Unassigned"),
    (252, "Unassigned"),
    (253, "Unassigned"),
    (254, "Unassigned"),
    (255, "Unassigned"),
    (256, "Unassigned"),
    (257, "Unassigned"),
    (258, "Unassigned"),
    (259, "Unassigned"),
    (260, "Unassigned"),
    (261, "Unassigned"),
    (262, "Unassigned"),
    (263, "Unassigned"),
    (264, "Unassigned"),
    (265, "Unassigned"),
    (266, "Unassigned"),
    (267, "Unassigned"),
    (268, "Unassigned"),
    (269, "Unassigned"),
    (270, "Unassigned"),
    (271, "Unassigned"),
    (272, "Unassigned"),
    (273, "Unassigned"),
    (274, "Unassigned"),
    (275, "Unassigned"),
    (276, "Unassigned"),
    (277, "Unassigned"),
    (278, "Unassigned"),
    (279, "Unassigned"),
    (280, "Unassigned"),
    (281, "Unassigned"),
    (282, "Unassigned"),
    (283, "Unassigned"),
    (284, "Unassigned"),
    (285, "Unassigned"),
    (286, "Unassigned"),
    (287, "Unassigned"),
    (288, "Unassigned"),
    (289, "Unassigned"),
    (290, "Unassigned"),
    (291, "Unassigned"),
    (292, "Unassigned"),
    (293, "Unassigned"),
    (294, "Unassigned"),
    (295, "Unassigned"),
    (296, "Unassigned"),
    (297, "Unassigned"),
    (298, "Unassigned"),
    (299, "Unassigned"),

    (309, "(Unused"),

    (309, "Unassigned"),
    (310, "Unassigned"),
    (311, "Unassigned"),
    (312, "Unassigned"),
    (313, "Unassigned"),
    (314, "Unassigned"),
    (315, "Unassigned"),
    (316, "Unassigned"),
    (317, "Unassigned"),
    (318, "Unassigned"),
    (319, "Unassigned"),
    (320, "Unassigned"),
    (321, "Unassigned"),
    (322, "Unassigned"),
    (323, "Unassigned"),
    (324, "Unassigned"),
    (325, "Unassigned"),
    (326, "Unassigned"),
    (327, "Unassigned"),
    (328, "Unassigned"),
    (329, "Unassigned"),
    (330, "Unassigned"),
    (331, "Unassigned"),
    (332, "Unassigned"),
    (333, "Unassigned"),
    (334, "Unassigned"),
    (335, "Unassigned"),
    (336, "Unassigned"),
    (337, "Unassigned"),
    (338, "Unassigned"),
    (339, "Unassigned"),
    (340, "Unassigned"),
    (341, "Unassigned"),
    (342, "Unassigned"),
    (343, "Unassigned"),
    (344, "Unassigned"),
    (345, "Unassigned"),
    (346, "Unassigned"),
    (347, "Unassigned"),
    (348, "Unassigned"),
    (349, "Unassigned"),
    (350, "Unassigned"),
    (351, "Unassigned"),
    (352, "Unassigned"),
    (353, "Unassigned"),
    (354, "Unassigned"),
    (355, "Unassigned"),
    (356, "Unassigned"),
    (357, "Unassigned"),
    (358, "Unassigned"),
    (359, "Unassigned"),
    (360, "Unassigned"),
    (361, "Unassigned"),
    (362, "Unassigned"),
    (363, "Unassigned"),
    (364, "Unassigned"),
    (365, "Unassigned"),
    (366, "Unassigned"),
    (367, "Unassigned"),
    (368, "Unassigned"),
    (369, "Unassigned"),
    (370, "Unassigned"),
    (371, "Unassigned"),
    (372, "Unassigned"),
    (373, "Unassigned"),
    (374, "Unassigned"),
    (375, "Unassigned"),
    (376, "Unassigned"),
    (377, "Unassigned"),
    (378, "Unassigned"),
    (379, "Unassigned"),
    (380, "Unassigned"),
    (381, "Unassigned"),
    (382, "Unassigned"),
    (383, "Unassigned"),
    (384, "Unassigned"),
    (385, "Unassigned"),
    (386, "Unassigned"),
    (387, "Unassigned"),
    (388, "Unassigned"),
    (389, "Unassigned"),
    (390, "Unassigned"),
    (391, "Unassigned"),
    (392, "Unassigned"),
    (393, "Unassigned"),
    (394, "Unassigned"),
    (395, "Unassigned"),
    (396, "Unassigned"),
    (397, "Unassigned"),
    (398, "Unassigned"),
    (399, "Unassigned"),

    (418, "Unassigned"),
    (419, "Unassigned"),
    (420, "Unassigned"),
    (421, "Unassigned"),
    
    (425, "Unassigned"),
    (427, "Unassigned"),
    (430, "Unassigned"),

    (432, "Unassigned"),
    (433, "Unassigned"),
    (434, "Unassigned"),
    (435, "Unassigned"),
    (436, "Unassigned"),
    (437, "Unassigned"),
    (438, "Unassigned"),
    (439, "Unassigned"),
    (440, "Unassigned"),
    (441, "Unassigned"),
    (442, "Unassigned"),
    (443, "Unassigned"),
    (444, "Unassigned"),
    (445, "Unassigned"),
    (446, "Unassigned"),
    (447, "Unassigned"),
    (448, "Unassigned"),
    (449, "Unassigned"),
    (450, "Unassigned"),
    (451, "Unassigned"),
    (452, "Unassigned"),
    (453, "Unassigned"),
    (454, "Unassigned"),
    (455, "Unassigned"),
    (456, "Unassigned"),
    (457, "Unassigned"),
    (458, "Unassigned"),
    (459, "Unassigned"),
    (460, "Unassigned"),
    (461, "Unassigned"),
    (462, "Unassigned"),
    (463, "Unassigned"),
    (464, "Unassigned"),
    (465, "Unassigned"),
    (466, "Unassigned"),
    (467, "Unassigned"),
    (468, "Unassigned"),
    (469, "Unassigned"),
    (470, "Unassigned"),
    (471, "Unassigned"),
    (472, "Unassigned"),
    (473, "Unassigned"),
    (474, "Unassigned"),
    (475, "Unassigned"),
    (476, "Unassigned"),
    (477, "Unassigned"),
    (478, "Unassigned"),
    (479, "Unassigned"),
    (480, "Unassigned"),
    (481, "Unassigned"),
    (482, "Unassigned"),
    (483, "Unassigned"),
    (484, "Unassigned"),
    (485, "Unassigned"),
    (486, "Unassigned"),
    (487, "Unassigned"),
    (488, "Unassigned"),
    (489, "Unassigned"),
    (490, "Unassigned"),
    (491, "Unassigned"),
    (492, "Unassigned"),
    (493, "Unassigned"),
    (494, "Unassigned"),
    (495, "Unassigned"),
    (496, "Unassigned"),
    (497, "Unassigned"),
    (498, "Unassigned"),
    (499, "Unassigned"),
    (509, "Unassigned")
]
