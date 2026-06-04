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

Assignment 2 candidate migration, batch 3:

- Attempt started: 2026-06-03
- `DensoVP6242` from DENSO VP6242 student model, Group_76, 2023S; active class includes two fixed intermediate visual links.
- `DensoVS068` from DENSO VS068, Khoa_A2_7, 2024S.
- `DobotCR10` from Dobot CR10, Group_58, 2023S.
- `DobotNova2` from Dobot Nova2, Danial_A2_2, 2024S.
- `FanucM20` from FANUC M-20, Group_82, 2023S; wrist/end-flange visuals simplified and final offsets tightened using ROS-Industrial M-20iA frame spacing because the submitted end geometry was not reliably aligned with the DH chain.
- `IgusReBel` from igus ReBeL with student rail variant, Danial_A2_6, 2024S.
- `KukaLBRiiwa14` from KUKA LBR iiwa 14, Group_51, 2023S; Robotiq gripper assets omitted.
- `ABBIRB1520ID` from ABB IRB 1520ID, Tony_A2_1, 2024S; submitted terminal tool offset shortened so the visual wrist flange remains attached to the arm.
- `ABBIRB1660ID` from ABB IRB 1660ID with student rail variant, Group_63, 2023S; student rail joint omitted and DH signs corrected to keep the global-home arm meshes attached while moving.

These models are staged for visual inspection in `tests/view_student_candidate_robots_batch3_swift.py` and are not yet exported through the main `ir_support_extra_robots.robots.__all__` list.

Assignment 2 candidate migration, batch 4:

- Attempt started: 2026-06-03
- `DoosanA0509` from Doosan A0509, Group_75, 2023S; original stem `A0509`.
- `DobotNova5` from Dobot Nova5, Group_49, 2023S.
- `UR16e` from Universal Robots UR16e, Group_72, 2023S, with related 2024S sources identified in the audit; DAE assets downsampled to keep package size manageable.
- `OmronTM12` from Omron TM12, Group_1 and Group_37, 2023S; DAE assets downsampled to keep package size manageable, and an attached suction-tool mesh was removed from the final link to better match the bare robot.
- `OmronTM5700` from Omron TM5-700, Group_14, 2023S, with related sources from Group_21 and Mahdi_A2_5 identified in the audit; DAE assets downsampled to keep package size manageable.
- `KukaKR4` from KUKA KR4, Group_41, 2023S.
- `KukaKR5Arc` from KUKA KR5 Arc STL assets in Danial_A2_5 and related 2024S submissions; STL assets were converted to DAE and assigned KUKA-style visual colours.
- `KukaKR6R900` from KUKA KR6 R900, Group_61, 2023S.
- `KukaTitan` from KUKA Titan, Karlos_A2_1, 2024S; DAE assets were normalized from millimetres to metres and treated as global-at-home meshes.
- `BCN3DMoveo` from BCN3D Moveo, Group_36, 2023S; the base PLY required an STL fallback conversion because Blender rejected the source PLY face-index type. Materials were set to an approximate BCN3D dark-body/blue-accent scheme and marked double-sided for Swift viewing. Link 2 remains visibly hollow in places because the student mesh includes open U-bracket geometry.

These models are staged for visual inspection in `tests/view_student_candidate_robots_batch4_swift.py` and are not yet exported through the main `ir_support_extra_robots.robots.__all__` list.

Assignment 2 candidate migration, batch 5:

- Attempt started: 2026-06-04
- Visual inspection accepted on 2026-06-04 for `Pulse75`, `MotomanGP7`, `FanucCRX10IAL`, `ABBIRB6740_260_300`, `OmronTM5900`, `KukaKR6R700CR`, and `KukaKR10`. `Pulse90` was rejected.
- `Pulse75` from Rozum Robotics PULSE 75, Group_68, 2023S; rail-style prismatic first joint removed, rail plates and the remaining low thin plate trimmed from the base mesh, and base lowered onto the xy plane for the IR Support candidate model.
- `Pulse90` was attempted from Rozum Robotics PULSE 90, Group_52, 2023S, but rejected on 2026-06-04 because the DH parameters, base pose, and DAE link locations could not be reconciled into a usable Swift model.
- `MotomanGP7` from Yaskawa Motoman GP7, A2_Tony_14_JonathanD_RhysH, 2025S; selected as a cleaner GP7 DAE source than the larger shortlist PLY set.
- `FanucCRX10IAL` from FANUC CRX-10iA/L, A2_AnhMinh_42_DaniyaS_ZainK, 2025S; using the smaller v2 DAE mesh set and the submitted identity CAD calibration transforms.
- `ABBIRB6740_260_300` from ABB IRB 6740-260/3.00, A2_Tony_19_JaidenP_VuNhatMinhH, 2025S.
- `OmronTM5900` from Omron TM5-900, Group_70, 2023S; using the full TM5 link mesh set.
- `KukaKR6R700CR` from KUKA KR6 R700 CR, Group_8, 2023S.
- `KukaKR10` from KUKA KR10, Khoa_A2_8, 2024S; using the Draft 3 link mesh set. Link 6 flat end-effector mounting plate was replaced with a small circular wrist flange, and link 1/2 triangles were duplicated with reversed winding for geometric double-sided viewing.

These batch 5 models have passed visual inspection for the optional extra robot package and are not promoted into the core lab model set.


Assignment 2 candidate migration, batch 6:

- Attempt started: 2026-06-05
- `OmronTM12X` from Omron/Techman TM12X, Group_69, 2023S.
- `KukaK6R900` from KUKA K6 R900, Sheila_A2_2, 2024S.
- `Kuka361` from a KUKA-style student model named Kuka361/Kuker, Katia_A2_2, 2024S; exact commercial model identity has not been verified.
- `KukaAgilusKR` from a KUKA Agilus-family KR candidate, Group_33, 2023S; the source comment identifies the family but not the exact variant.
- `JakaZu3` from JAKA Zu3, Group_24, 2023S; the source cites JAKA Zu3 STEP files and published DH parameters.
- `UniversalRobotsURP` was attempted from a student source named URP / Universal Robot 3 kg payload, Group_12, 2023S, then rejected after review. Universal Robots documents the 3 kg payload model as UR3e, not URP, and the student meshes/kinematics did not match a recognisable off-the-shelf UR robot.
- Generic `fanuc`, Richardo/Emily/Thomais/Mark, `PR2`, and `THOR` shortlist entries were not imported in this batch because they were duplicates, not clearly industrial-arm candidates, or not identifiable enough for a clean package name.
