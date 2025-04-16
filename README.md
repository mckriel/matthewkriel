# Schedule Monitoring System

This system provides detailed logging for class schedule changes, which should help identify the cause of schedule reverts.

## Key Features

1. **Comprehensive Logging**: Every change to class schedules is now logged to files in the 'logs' directory
2. **Middleware Logging**: All requests, responses, and database operations for the PFA app are logged
3. **Model Change Tracking**: Django signals track every create/update/delete operation
4. **Admin Action Logging**: Admin panel actions now include detailed logs
5. **Schedule Snapshot Tool**: A management command can detect unauthorized schedule changes

## Usage Instructions

### Monitoring Logs

Log files are stored in the 'logs' directory:
- pfa.log - All PFA app actions
- db_operations.log - Database operations
- admin_actions.log - Admin user actions

### Detecting Schedule Changes

Run the following command to detect any unauthorized changes:

Running schedule change detection...
No previous snapshot found. Creating initial snapshot.
Schedule snapshot saved

This will compare current schedules with the previous snapshot and report differences.

### Checking Recently Modified Classes

To see which classes were modified in the last few days:

No classes have been modified in the last 7 days.

## Troubleshooting

If you notice schedule reverts:
1. Check the logs for any unexpected changes
2. Look for patterns in admin_actions.log that might indicate another admin making changes
3. Review db_operations.log for any automated operations affecting the schedules
4. Check system cron jobs or scheduled tasks that might be running database backups/restores
