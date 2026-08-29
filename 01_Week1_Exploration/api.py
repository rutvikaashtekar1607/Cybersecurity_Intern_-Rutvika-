# api.py - Flask REST API
from flask import Flask, jsonify, request
from rule_engine import rule_engine
from logger import logger
from alerts import alert_engine
import ai_assist
import json

app = Flask(__name__)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(logger.get_stats())

@app.route('/api/rules', methods=['GET'])
def get_rules():
    return jsonify({"rules": rule_engine.list_rules()})

@app.route('/api/rules', methods=['POST'])
def add_rule():
    data = request.json
    
    # VALIDATE the input first
    is_valid, message = validate_rule(data)
    if not is_valid:
        return jsonify({'error': message, 'status': 'validation_failed'}), 400
        
    # Now add the validated rule
    rule = {
        'action': data['action'],
        'protocol': data['protocol'],
        'port': int(data['port']),
        'description': data['description']
    }
    firewall.add_rule(rule)
    return jsonify({'status': 'success', 'message': 'Rule added', 'rule': rule}), 201

@app.route('/api/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    rule_engine.delete_rule(rule_id)
    return jsonify({"success": True})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    count = request.args.get('count', 10, type=int)
    logs = logger.get_recent_logs(count)
    return jsonify({"logs": logs})

@app.route('/api/logs/export', methods=['POST'])
def export_logs():
    output_file = request.json.get('filename', 'firewall_logs_export.json')
    logger.export_logs(output_file)
    return jsonify({"success": True, "file": output_file})

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    alerts = alert_engine.all_alerts()
    return jsonify({'alerts': alerts})

@app.route('/api/ai/recommend', methods=['GET'])
def ai_recommend():
    logs = logger.get_recent_logs(200)
    return jsonify(ai_assist.recommend_rules(logs))

@app.route('/api/ai/summarize-anomalies', methods=['GET'])
def ai_summarize_anomalies():
    return jsonify({"summary": ai_assist.summarize_traffic_anomalies(alert_engine.all_alerts())})

@app.route('/api/ai/summarize-logs', methods=['GET'])
def ai_summarize_logs():
    logs = logger.get_recent_logs(200)
    return jsonify({"summary": ai_assist.summarize_logs(logs)})

@app.route('/api/ai/explain/<int:rule_id>', methods=['GET'])
def ai_explain(rule_id):
    rules = rule_engine.list_rules()
    rule = next((r for r in rules if r["id"] == rule_id), None)
    if not rule:
        return jsonify({"error": "rule not found"}), 404
    return jsonify({"explanation": ai_assist.explain_policy(rule)})

@app.route('/api/ai/risk/<source_ip>', methods=['GET'])
def ai_risk(source_ip):
    return jsonify(ai_assist.score_risk(source_ip, alert_engine.all_alerts()))

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Firewall API Running", "version": "1.0"})

def validate_rule(data):
    """Validate rule data before adding to firewall"""
    # Check required fields exist
    required_fields = ['action', 'protocol', 'port', 'description']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        
    if data['action'] not in ['ALLOW', 'DROP']:
        return False, f"Invalid action '{data['action']}'. Must be 'ALLOW' or 'DROP'"
        
    if data['protocol'] not in ['TCP', 'UDP']:
        return False, f"Invalid protocol '{data['protocol']}'. Must be 'TCP' or 'UDP'"
        
    try:
        port = int(data['port'])
        if port < 1 or port > 65535:
            return False, f"Invalid port {port}. Must be between 1-65535"
    except (ValueError, TypeError):
        return False, f"Port must be a number, got '{data['port']}'"
        
    if not isinstance(data['description'], str) or len(data['description']) == 0:
        return False, "Description must be a non-empty string"
        
    return True, "Valid"

if __name__ == '__main__':
    print("[*] Starting Firewall REST API on http://localhost:5000")
    app.run(debug=True, port=5000)
