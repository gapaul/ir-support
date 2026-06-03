# Model Provenance

This optional robot pack contains visually useful models that are not required by the core 41013 lab exercises, quizzes, or assignments. They are included as teaching assets and should be treated cautiously rather than as manufacturer-verified reference models.

Two broad sources are represented here:

- Older UTS MATLAB Robotics Toolbox models, made by UTS staff and students between about 2016 and 2022, then ported from the local MATLAB toolbox archive into Python/Swift-ready DAE assets.
- Newer candidate models derived from promising 41013 Robotics Assignment 2 submissions, moved across after an audit of the 2023S, 2024S, and 2025S student project folders.

Assignment 2 candidate migration:

- Attempt started: 2026-05-31 20:29:07 +10:00
- Reorganised into `ir_support_extra_robots`: 2026-06-01

Selected student-derived models:

- `AuboI5` from Aubo i5, Group_11, 2023S; original stem `Auboi5`.
- `ABBCRB15000` from ABB GoFa / CRB 15000, Group_39, 2023S; original stem `CRB15000`.
- `ABBGoFa10` from ABB GoFa 10, Group_13, 2023S; original stem `GoFa10`.
- `DobotCR3` from Dobot CR3, Group_28, 2023S; original stem `CR3`.
- `DobotCR5` from Dobot CR5, Group_23, 2023S; original stem `DobotCR5`.
- `DobotCR16` from Dobot CR16, Group_103, 2023S; original stem `DobotCR16`.
- `FanucCRX10IA` from FANUC CRX-10iA, Victor_A2_9, 2024S; final fixed gripper link omitted from DH chain; original stem `CRX10IA`.
- `FanucCRX5IA` from FANUC CRX-5iA candidate, Group_9, 2023S; original stem `Fanuc5iA`.
- `FanucLRMate200iD` from FANUC LR Mate 200iD, Tony_A2_2, 2024S; original stem `Fanuc200iD`.
- `YaskawaGP4` from Yaskawa GP4, Group_48, 2023S; original stem `YaskawaGP4`.

Assignment 2 candidate migration, batch 2:

- Attempt started: 2026-06-03
- `ABBIRB2600` from ABB IRB2600, A2_Khoa_51_MarcusF_HarrshawarthanG_YutoB, 2025S.
- `KukaKR3R540` from KUKA KR3 540, A2_Khoa_51_MarcusF_HarrshawarthanG_YutoB, 2025S.
- `KukaKR10R1100` from KUKA KR10 R1100, A2_Tony_12_AbishaN_JessicaL_AryaD, 2025S.
- `EpsonVT6` from Epson VT6, A2_Tony_12_AbishaN_JessicaL_AryaD, 2025S.
- `FanucLRMate200iC` from FANUC LR Mate 200iC, A2_Khoa_51_MarcusF_HarrshawarthanG_YutoB, 2025S.
- `KukaKR60` from KUKA KR60, A2_Khoa_51_MarcusF_HarrshawarthanG_YutoB, 2025S.
- `UnitreeZ1` from Unitree Z1, A2_Tan_8_DineshS_DanishS_MahakS, 2025S.
- `ProSixVT6` from Epson ProSix VT6, A2_Tan_8_DineshS_DanishS_MahakS, 2025S.
- `MyCobot320` from Elephant Robotics MyCobot 320, A2_Tan_8_DineshS_DanishS_MahakS, 2025S.
- `MitsubishiRV2RF` from Mitsubishi RV-2FR, A2_Khoa_57_HongLinhN_NhatMinhV, 2025S.

These models are staged for visual inspection in `tests/view_student_candidate_robots_batch2_swift.py` and are not yet exported through the main `ir_support_extra_robots.robots.__all__` list.
