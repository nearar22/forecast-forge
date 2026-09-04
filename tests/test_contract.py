import hashlib,json
CONTRACT="contracts/contract.py";QUESTION="Will the City Alpha open-data portal publish its audited 2026 accessibility report before October 1, 2026?";OUTCOMES=["YES","NO"];CRITERIA="Resolve YES only if the city portal or auditor publishes a dated final report before the deadline. Drafts and social posts do not qualify. Resolve NO after the deadline; use UNRESOLVED if two independent snapshots cannot verify either condition."
def make(c,vm,alice):vm.sender=alice;return c.create_market(QUESTION,OUTCOMES,CRITERIA,2)
def digest(mid,outcome,confidence,nonce):return hashlib.sha256((mid+":"+outcome+":"+str(confidence)+":"+nonce).encode()).hexdigest()
CITY_TEXT="City portal final report confirms the audited publication date and accessibility result."
AUDIT_TEXT="Independent auditor index confirms the final report and exact publication deadline."
def page_hash(text):return hashlib.sha256(" ".join(text.split()).encode()).hexdigest()
def evidence(c,vm,mid):
 vm.mock_web("https://city.example/report",{"method":"GET","status":200,"body":CITY_TEXT});vm.mock_web("https://auditor.example/index",{"method":"GET","status":200,"body":AUDIT_TEXT})
 c.submit_evidence(mid,"https://city.example/report","https://archive.example/report",page_hash(CITY_TEXT),"2026-09-01T12:00:00Z");c.submit_evidence(mid,"https://auditor.example/index","",page_hash(AUDIT_TEXT),"2026-09-01T12:05:00Z")
def result(vm,outcome="YES",confidence=90):vm.mock_llm("FORECASTFORGE",json.dumps({"outcome":outcome,"confidence":confidence,"rationale":"Two independent snapshots satisfy the exact publication criteria and deadline.","source_findings":["City source confirms publication","Auditor index confirms final report"]}))
def test_market_validation_and_one_commit_per_wallet(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice
 with direct_vm.expect_revert("exact criteria"):c.create_market("Too short",["YES","NO"],"vague",2)
 mid=make(c,direct_vm,direct_alice);direct_vm.sender=direct_bob;c.commit_forecast(mid,digest(mid,"YES",80,"n"))
 with direct_vm.expect_revert("already committed"):c.commit_forecast(mid,"a"*64)
def test_sealed_reveal_and_snapshot_guards(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=direct_deploy(CONTRACT);mid=make(c,direct_vm,direct_alice);direct_vm.sender=direct_bob;fid=c.commit_forecast(mid,digest(mid,"YES",80,"n"));assert c.get_forecast(fid)["outcome"]=="";direct_vm.warp("2026-09-06T12:00:00Z");direct_vm.sender=direct_bob;c.open_reveal(mid)
 with direct_vm.expect_revert("does not match"):c.reveal_forecast(fid,"NO",80,"n")
 c.reveal_forecast(fid,"YES",80,"n");direct_vm.warp("2026-09-08T12:00:00Z");direct_vm.sender=direct_bob;c.open_evidence(mid)
 with direct_vm.expect_revert("public HTTPS source"):c.submit_evidence(mid,"http://bad.example","","x","today")
 evidence(c,direct_vm,mid);assert len(c.get_market(mid)["evidence"])==2
 with direct_vm.expect_revert("distinct source host"):c.submit_evidence(mid,"https://city.example/other","","c"*64,"2026-09-01T12:10:00Z")
def test_consensus_finalize_and_portable_accuracy(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=direct_deploy(CONTRACT);mid=make(c,direct_vm,direct_alice);direct_vm.sender=direct_bob;fid=c.commit_forecast(mid,digest(mid,"YES",85,"x"));direct_vm.warp("2026-09-06T12:00:00Z");direct_vm.sender=direct_bob;c.open_reveal(mid);c.reveal_forecast(fid,"YES",85,"x");direct_vm.warp("2026-09-08T12:00:00Z");c.open_evidence(mid);evidence(c,direct_vm,mid);direct_vm.warp("2026-09-10T12:00:00Z");result(direct_vm);r=c.resolve_market(mid);direct_vm.clear_mocks();assert r["outcome"]=="YES" and r["confidence"]==90
 with direct_vm.expect_revert("before appeal deadline"):c.finalize_market(mid)
 direct_vm.warp("2026-09-13T12:00:00Z");direct_vm.sender=direct_bob;c.finalize_market(mid);p=c.get_profile(direct_bob);assert p["accuracy"]==100 and p["correct"]==1
def test_unresolved_is_neutral_and_single_appeal(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=direct_deploy(CONTRACT);mid=make(c,direct_vm,direct_alice);direct_vm.sender=direct_bob;fid=c.commit_forecast(mid,digest(mid,"NO",60,"x"));direct_vm.warp("2026-09-06T12:00:00Z");direct_vm.sender=direct_bob;c.open_reveal(mid);c.reveal_forecast(fid,"NO",60,"x");direct_vm.warp("2026-09-08T12:00:00Z");c.open_evidence(mid);evidence(c,direct_vm,mid);direct_vm.warp("2026-09-10T12:00:00Z");result(direct_vm,"UNRESOLVED",35);c.resolve_market(mid);direct_vm.mock_web("https://appeal.example/new",{"method":"GET","status":200,"body":"New independent archive provides later evidence for the same market criteria."});c.submit_evidence(mid,"https://appeal.example/new","",page_hash("New independent archive provides later evidence for the same market criteria."),"2026-09-10T13:00:00Z");c.appeal_resolution(mid,"New archived evidence was submitted for reconsideration.");direct_vm.clear_mocks()
 with direct_vm.expect_revert("Appeal needs new evidence"):c.appeal_resolution(mid,"Try the same appeal a second time with no new rights.")
 direct_vm.warp("2026-09-13T12:00:00Z");c.finalize_market(mid);assert c.get_profile(direct_bob)["resolved"]==0
def test_changed_snapshots_fail_closed_without_llm_ruling(direct_vm,direct_deploy,direct_alice,direct_bob):
 c=direct_deploy(CONTRACT);mid=make(c,direct_vm,direct_alice);direct_vm.sender=direct_bob;c.commit_forecast(mid,digest(mid,"YES",70,"recovery"));direct_vm.warp("2026-09-06T12:00:00Z");c.open_reveal(mid);direct_vm.warp("2026-09-08T12:00:00Z");c.open_evidence(mid)
 direct_vm.mock_web("https://one.example/report",{"method":"GET","status":200,"body":"Current content no longer matches the submitted snapshot."});direct_vm.mock_web("https://two.example/report",{"method":"GET","status":200,"body":"Second source also changed after its snapshot was recorded."})
 c.submit_evidence(mid,"https://one.example/report","","a"*64,"2026-09-08T12:00:00Z");c.submit_evidence(mid,"https://two.example/report","","b"*64,"2026-09-08T12:05:00Z");direct_vm.warp("2026-09-10T12:00:00Z");r=c.resolve_market(mid);direct_vm.clear_mocks()
 assert r["outcome"]=="UNRESOLVED" and r["confidence"]==0
