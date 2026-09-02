import json,os,sys,time
sys.path.insert(0,os.path.dirname(__file__));import patch_status;patch_status.apply();from gl import make_client,read_view
TERMINAL={"ACCEPTED","FINALIZED","UNDETERMINED","CANCELED"}
def wait(client,tx):
 for _ in range(160):
  try:
   item=client.get_transaction(transaction_hash=tx);status=str(item.get("status_name") or item.get("status"));print(status,flush=True)
   if status in TERMINAL:return status
  except Exception as exc:print("poll",exc,flush=True)
  time.sleep(8)
 return "TIMEOUT"
def main():
 root=os.path.dirname(os.path.dirname(__file__));address=json.load(open(os.path.join(root,"deployment.json")))["address"];client,account=make_client();question="Will the City Alpha open-data portal publish its audited 2026 accessibility report before October 1, 2026?";criteria="Resolve YES only if the city portal or its independent auditor publishes a dated final report before the deadline. Drafts and social posts do not qualify. Resolve NO after the deadline, and UNRESOLVED if two independent snapshots cannot verify either condition."
 tx=client.write_contract(address=address,function_name="create_market",args=[question,["YES","NO"],criteria,2],value=0);print("tx",tx);status=wait(client,tx);market=read_view(client,account,address,"get_market",["market-1"]);out={"status":status,"market":{"id":market.get("id"),"phase":market.get("phase"),"min_evidence":market.get("min_evidence"),"outcomes":market.get("outcomes")},"stats":read_view(client,account,address,"get_stats")};open(os.path.join(root,"scripts","live_verification.json"),"w",encoding="utf-8").write(json.dumps(out,indent=2,default=str));print(json.dumps(out,indent=2,default=str))
if __name__=="__main__":main()
