#!/bin/bash
# shellcheck disable=SC2001,SC2086,SC2155

################################################################################
# Submitter Starter Script
#
# What this script does:
# - Generates task-specific artifacts (output.json/state.json/tree.txt)
# - Bundles required files into <SUBMISSION_USERNAME>.tar.gz
# - Uploads to the AGS endpoint
#
# What to customize:
# - projectId / lmsName / artifactVersion
# - per-task sail2taskid + secretKey mapping (in the -t handler)
# - submit_task{1,2,3} TODO blocks (safe to edit; tests may rely on output keys)
#
################################################################################

set -u  # treat unset variables as error (but we do NOT use `set -e` globally because task1 has its own handler)

################################################################################
################  PREP FOR CLOUD NATIVE (EDIT ME)   ############################
################################################################################

projectId="project-author-auto-scali-ppzdmwjh"     #
taskId=""                                         # set by -t option
secretKey=""                                      # set by -t option
lmsName="sail2"                                   #
artifactVersion="v1"                              # TODO: bump for new releases

# Generic context required by AGS
studentDNS=$(curl --silent ipinfo.io/ip)
ags_dns="autograding.sailplatform.org"
signature="1K9SaGliHwthRgeOi12hUdCUwAPmN"
duration=120

# =========================
# Per-task config (EDIT ME)
# =========================
TASK1_SAIL2TASKID="637f46f7-6454-4c48-9028-5b31d03f2d99"
TASK1_SECRETKEY="statefulsets-for-mysql-IXvtV6WoQq"

TASK2_SAIL2TASKID="6519fcac-e5e2-46a0-ad07-f2ee8cd6d6e8"
TASK2_SECRETKEY="separate-reader-+-writer-for-mysql-cn2h9wV1UC"

TASK3_SAIL2TASKID="9b32d4a9-5451-48d7-b142-606bb27434c6"
TASK3_SECRETKEY="horizontal-autoscaling-NqPumi758S"



################################################################################
############################ Shared Utilities ##################################
################################################################################

log() { echo -e "$*"; }

cecho(){
    # Regular Colors
    Black='\033[0;30m'        # Black
    Red='\033[0;31m'          # Red
    Green='\033[0;32m'        # Green
    Yellow='\033[0;33m'       # Yellow
    Blue='\033[0;34m'         # Blue
    Purple='\033[0;35m'       # Purple
    Cyan='\033[0;36m'         # Cyan
    White='\033[0;37m'        # White

    NC="\033[0m" # No Color

    # printf "${(P)1}${2} ${NC}\n" # <-- zsh
    printf "${!1}${2} ${NC}\n" # <-- bash
}

# === Utility: simple progress bar ===
progress_bar() {
  local duration=$1
  local interval=0.1
  local width=30
  local elapsed=0

  while (( $(echo "$elapsed < $duration" | bc -l) )); do
    local filled
    filled=$(printf "%.0f" "$(echo "$elapsed * $width / $duration" | bc -l)")
    printf "\r[%-${width}s] %3d%%" "$(printf '#%.0s' $(seq 1 $filled))" "$(echo "$elapsed * 100 / $duration" | bc)"
    sleep $interval
    elapsed=$(echo "$elapsed + $interval" | bc)
  done

  printf "\r[%-${width}s] 100%%\n" "$(printf '#%.0s' $(seq 1 $width))"
}

# Writes a directory tree if possible (non-fatal if `tree` missing)
write_tree() {
  (tree > tree.txt 2>/dev/null || echo "tree command not available, skipping..." > tree.txt)
}

# JSON-safe string via jq (required)
json_str() {
  # usage: json_str "$value"
  jq -Rn --arg v "$1" '$v'
}

# Common cleanup for task1 container
stop_container_if_running() {
  local container_name="$1"
  docker stop "$container_name" >/dev/null 2>&1 || true
}

global_clean_up() {
  rm -f "${submissionUsername}.tar.gz" 2>/dev/null || true
  # rm -f tree.txt output.json state.json 2>/dev/null || true
}






################################################################################
############################ Task 1 Submitter ##################################
################################################################################
submit_task1() {
  log "=== Starting Task 1 Submission ==="

  # Step 1: JWT Token
  log "Retrieving JWT token..."
  local EXTERNAL_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
  local TOKEN_OUTPUT=""
  if [[ -n "$EXTERNAL_IP" ]]; then
    TOKEN_OUTPUT=$(curl -m 5 -s -H 'Content-Type: application/json' -d '{"username":"admin", "password":"asdasd"}' -X POST "http://$EXTERNAL_IP/v1/logintoken" || true)
  fi
  echo "$TOKEN_OUTPUT" > output1.json
  if ! jq empty output1.json 2>/dev/null; then
    log "\n❌ ERROR: JWT token request did not return valid JSON (output1.json)."
    log "   Response preview: $(head -c 200 output1.json)"
    log "   Check that your login service is reachable at http://$EXTERNAL_IP/v1/logintoken"
    exit 1
  fi
  progress_bar 2

  # Step 2: MySQL Version
  log "Retrieving MySQL version..."
  local MYSQL_VER=""
  MYSQL_VER=$(kubectl exec deploy/login -- python manage.py shell -c "from django.db import connection; cm = connection.cursor(); cursor = cm.__enter__(); cursor.execute('SELECT VERSION();'); print(cursor.fetchone()[0]); cursor.close()" 2>/dev/null | tail -n 1 | tr -d '\r' || true)
  if [[ -z "$MYSQL_VER" || "$MYSQL_VER" == *"Traceback"* ]]; then
    log "\n❌ ERROR: Could not retrieve MySQL version from Django pod."
    log "   Check that the login deployment is running and can connect to MySQL."
    exit 1
  fi
  echo "{\"version\": \"$MYSQL_VER\"}" > output2.json
  progress_bar 2

  # Step 3: Directory tree
  log "Running other checks..."
  write_tree
  progress_bar 1
}

################################################################################
############################ Task 2 Submitter ##################################
################################################################################
submit_task2() {
  log "=== Starting Task 2 Submission ==="

  # Step 1: JWT Token
  log "Retrieving JWT token..."
  local EXTERNAL_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
  if [[ -z "$EXTERNAL_IP" ]]; then
    log "\n❌ ERROR: Could not find the Istio ingress gateway LoadBalancer IP."
    log "   Check that istio-ingressgateway is deployed and has an external IP."
    exit 1
  fi
  local TOKEN_OUTPUT
  TOKEN_OUTPUT=$(curl -m 5 -s -H 'Content-Type: application/json' -d '{"username":"admin", "password":"asdasd"}' -X POST "http://$EXTERNAL_IP/v1/logintoken" || true)
  if ! echo "$TOKEN_OUTPUT" | jq empty 2>/dev/null; then
    log "\n❌ ERROR: JWT token request did not return valid JSON."
    log "   Response preview: $(echo "$TOKEN_OUTPUT" | head -c 200)"
    log "   Check that your login service is reachable at http://$EXTERNAL_IP/v1/logintoken"
    exit 1
  fi
  progress_bar 2

  # Step 2: MySQL Read-Only Status
  log "Retrieving read-only status from MySQL read replica (mysql-1)..."
  local READONLY_STATUS
  READONLY_STATUS=$(kubectl exec mysql-1 -c mysql -- mysql -uroot -prootpassword -e "SHOW VARIABLES LIKE 'read_only';" 2>/dev/null || true)
  if [[ -z "$READONLY_STATUS" ]]; then
    log "\n❌ ERROR: Could not retrieve read_only status from mysql-1."
    log "   Check that the mysql-1 pod is running and accessible."
    exit 1
  fi
  progress_bar 2

  log "Writing output.json..."
  jq -n --argjson a "$TOKEN_OUTPUT" --arg b "$READONLY_STATUS" '{a: $a, b: $b}' > output.json
  progress_bar 1

  # Step 3: Directory tree
  log "Running other checks..."
  write_tree
  progress_bar 1
}


submit_task3() {
  log "=== Starting Task 3 Submission ==="

  local replicas=$(kubectl get hpa -o json | jq '.items[0].spec.minReplicas')
  local readinessProbeCheck=$(kubectl get deployment login -o json | jq '.spec.template.spec.containers[0].readinessProbe.httpGet.path')
  local startupProbeCheck=$(kubectl get deployment login -o json | jq '.spec.template.spec.containers[0].startupProbe.httpGet.path')
  
  local output_json='{
  "replicas": "'"$replicas"'",
  "readinessProbeCheck": '$readinessProbeCheck',
  "startupProbeCheck": '$startupProbeCheck'
  }'

  echo "$output_json" > output.json
  progress_bar 1

  # wait till student has 1 pod (TEST LATER)
  log "Before scale-up, waiting for replicas to go down to 1"
  while true; do
      local replcias2=$(kubectl get deployment -o json | jq -r '.items[0].spec.replicas')
      if [ "$replcias2" -eq 1 ]; then
          log "Deployment has scaled to 1 pod."
          break
      else
          log "Waiting for deployment to scale to 1 pod..."
          sleep 5
      fi
  done    
  progress_bar 1

  local studentDNS=$(kubectl get svc -n istio-system istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

  log "Starting load test... This takes about 5 minutes."
  myenv/bin/locust -f llm_server/locustfile.py --headless -H http://$studentDNS -u 5 -r 0.008 --run-time 5m --csv testme

  local file_path="testme_stats_history.csv" 
  local line_count=0
  if [[ -f "$file_path" ]]; then
      line_count=$(wc -l < "$file_path")
  fi

  if [ "$line_count" -lt 140 ]; then
      log "Error: Your load test hasn't proceeded far enough for grading. If you see this and haven't exited the load-test, please let us know."
      rm -f testme_exceptions.csv testme_failures.csv testme_stats_history.csv testme_stats.csv output.json
      exit 1
  fi

  local failures=$(awk -F, '$2=="Aggregated" {print $4}' testme_stats.csv)
  if [[ -z "$failures" ]]; then failures=0; fi

  log "After scale up, waiting for system to scale back down to 1 pod."
  while true; do
      local replcias2=$(kubectl get deployment -o json | jq -r '.items[0].spec.replicas')
      if [ "$replcias2" -eq 1 ]; then
          log "Deployment has scaled to 1 pod."
          break
      else
          log "Waiting for deployment to scale to 1 pod..."
          sleep 5
      fi
  done    
  progress_bar 1

  echo '{"failures": "'"$failures"'"}' > output2.json

  jq -s '.' output.json output2.json > output1.tmp && mv output1.tmp output.json

  rm -f output2.json
  rm -f testme_exceptions.csv testme_failures.csv testme_stats_history.csv testme_stats.csv
  
  write_tree
  progress_bar 1
}

################################################################################
############################ Files to Submit ###################################
################################################################################
# This function is used by the packager to decide what to include.
# Exclusions are handled by only listing required paths.
find_files_to_submit() {
  if [ "$taskId" = "task1" ]; then
    task1files
  fi
  if [ "$taskId" = "task2" ]; then
    task2files
  fi
  if [ "$taskId" = "task3" ]; then
    task3files
  fi
}

task1files() {
  echo "output1.json"
  echo "output2.json"
  echo "tree.txt"
}

task2files() {
  echo "output.json"
  echo "tree.txt"
}

task3files() {
  echo "output.json"
  echo "tree.txt"
}


################################################################################
############################ Env + Args Parsing ################################
################################################################################

if [[ -z "${SUBMISSION_USERNAME:-}" ]]; then
  log "Please set SUBMISSION_USERNAME as your Sail() username first with the command:"
  log "export SUBMISSION_USERNAME=\"value\""
  exit 1
else
  submissionUsername="${SUBMISSION_USERNAME}"
fi

if [[ -z "${SUBMISSION_PASSWORD:-}" ]]; then
  log "Please set SUBMISSION_PASSWORD as your submission password from the Sail() platform with the command:"
  log "export SUBMISSION_PASSWORD=\"value\""
  exit 1
else
  submissionPassword="${SUBMISSION_PASSWORD}"
fi

while getopts ":ha:t:s:" opt; do
  case $opt in
    h)
      log "This program is used to submit and grade your solutions."
      log "Usage for Task 1: ./submitter -t task1"
      log "Usage for Task 2: ./submitter -t task2"
      log "Usage for Task 3: ./submitter -t task3"
      exit
      ;;
    t)
    taskId="$OPTARG"
    case "$taskId" in
      "task1")
        sail2taskid="$TASK1_SAIL2TASKID"
        secretKey="$TASK1_SECRETKEY"
        ;;
      "task2")
        sail2taskid="$TASK2_SAIL2TASKID"
        secretKey="$TASK2_SECRETKEY"
        ;;
      "task3")
        sail2taskid="$TASK3_SAIL2TASKID"
        secretKey="$TASK3_SECRETKEY"
        ;;
      *)
        echo "Unknown taskId"
        exit 1
        ;;
    esac
    ;;

      
    \?)
      log "Invalid option: -$OPTARG"
      exit 1
      ;;
  esac
done

################################################################################
############################ Integrity Pledge ##################################
################################################################################
log "####################"
log "# INTEGRITY PLEDGE #"
log "####################"
log "Have you cited all the reference sources (both people and websites) in the file named 'references'?"
log "Type \"I AGREE\" to continue."
read -r references

if [[ "$references" == "I AGREE" ]]; then

  if [ "$taskId" = "task1" ]; then
    submit_task1
  fi
  if [ "$taskId" = "task2" ]; then
    submit_task2
  fi
  if [ "$taskId" = "task3" ]; then
    submit_task3
  fi


  log "Uploading answers..."
  log "Files larger than 5M will be ignored."

  rm -f "${submissionUsername}.tar.gz"
  find_files_to_submit | tar -cvzf "${submissionUsername}.tar.gz" -T - &> /dev/null

  # Remove output.json after packaging (preserves original behavior)
  # rm -f output.json output1.json output2.json

  postUrl="https://${ags_dns}/submit?signature=${signature}&submissionUsername=${submissionUsername}&submissionPassword=${submissionPassword}&dns=${studentDNS}&projectId=${projectId}&taskId=${sail2taskid}&secretKey=${secretKey}&duration=${duration}&lmsName=${lmsName}&artifactVersion=${artifactVersion}"

  submitFile="${submissionUsername}.tar.gz"
  if ! curl -s -F file=@"$submitFile" "$postUrl"; then
    log "Submission failed, please check your password or try again later."
  else
    log "If your submission is uploaded successfully, log in to Sail() and check the submissions table."
  fi

  rm -f "${submissionUsername}.tar.gz"

else
  log "Please cite all detailed references in the file 'references' and submit again."
fi