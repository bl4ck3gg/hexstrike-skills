---
name: ctf-validation
when_to_use: 得到候选 flag 后
---
# CTF 验证步骤
Web: response_validation / payload_verification / flag_format_check / reproducibility_test
Crypto: decryption_verification / key_validation / mathematical_check / flag_extraction
Pwn: exploit_reliability / payload_verification / shell_validation / flag_retrieval
Forensics: data_integrity / timeline_accuracy / evidence_correlation / flag_location
Rev: algorithm_accuracy / key_extraction / solution_testing / flag_generation
OSINT: source_verification / cross_reference / accuracy_check / flag_confirmation
Misc: solution_verification / output_validation / edge_case_testing / flag_extraction

## flag 格式
flag\{...\}  FLAG\{...\}  ctf\{...\}  CTF\{...\}  [a-zA-Z0-9_]+\{...\}

## 资源估算
web{cpu:4,mem:4096,net:high} crypto{cpu:8,mem:8192,gpu:true} pwn{cpu:4,mem:4096} forensics{cpu:2,mem:8192,disk:4096} rev{cpu:4,mem:8192} osint{cpu:2,mem:2048} misc{cpu:2,mem:2048}
难度倍数: easy 1.0 / medium 1.2 / hard 1.5 / insane 2.0 / unknown 1.3
