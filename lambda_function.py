
import os
import json
import shutil
import sqlite3


def get_available_vacations_days(employee_id):

    db_path = "/tmp/employee_database.db"

    # Copy database from Lambda deployment package to /tmp
    if not os.path.exists(db_path):
        shutil.copy(
            os.path.join(
                os.path.dirname(__file__),
                "employee_database.db"
            ),
            db_path
        )

    conn = sqlite3.connect(db_path)

    try:
        cursor = conn.cursor()

        if not employee_id:
            raise ValueError("No employee id provided")

        cursor.execute("""
            SELECT employee_vacation_days_available
            FROM vacations
            WHERE employee_id = ?
            ORDER BY year DESC
            LIMIT 1
        """, (employee_id,))

        result = cursor.fetchone()

        if result:
            return result[0]

        return f"No vacation data found for employee_id {employee_id}"

    finally:
        conn.close()


def lambda_handler(event, context):

    print("Gateway event:")
    print(json.dumps(event))

    # ----------------------------------------
    # AgentCore Gateway event
    # ----------------------------------------
    if "tool_name" in event:

        tool_name = event["tool_name"]

        # Gateway may prefix the tool name with the target name.
        # We only need the actual tool name.
        tool_name = tool_name.split("__")[-1]

        if tool_name == "get_available_vacation_days":

            arguments = event.get("arguments", {})

            employee_id = arguments.get("employee_id")

            available_days = get_available_vacations_days(
                employee_id
            )

            return {
                "available_vacation_days": available_days
            }

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    # ----------------------------------------
    # Direct Lambda invocation
    # ----------------------------------------
    employee_id = event.get("employee_id")

    available_days = get_available_vacations_days(
        employee_id
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "employee_id": employee_id,
            "available_vacation_days": available_days
        })
    }
