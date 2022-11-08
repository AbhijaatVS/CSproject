# CSproject
Insure you have the Tabulate, datetime, maskpass, time and mysql.connector modules
Run it on the terminal, won't run on the shell.
You also need MySQL tables with the following structures:
1) Details

| Field    | Type        | Null | Key | Default | Extra |

| username | varchar(20) | NO   | PRI | NULL    |       |

| password | char(20)    | YES  |     | NULL    |       |

| balance  | bigint      | YES  |     | NULL    |       |

2) Statements

| Field               | Type         | Null | Key | Default | Extra |

| username            | varchar(20)  | NO   |     | NULL    |       |

| Statements          | varchar(300) | YES  |     | NULL    |       |

| MoneyDelta          | char(30)     | YES  |     | NULL    |       |

| balance             | bigint       | YES  |     | NULL    |       |

| Date_Of_Transaction | datetime     | YES  |     | NULL    |       |


3) Fixed_Deposits
| Field               | Type        | Null | Key | Default | Extra |

| username            | varchar(20) | NO   |     | NULL    |       |

| principal           | bigint      | YES  |     | NULL    |       |

| rate                | int         | YES  |     | NULL    |       |

| duration            | int         | YES  |     | NULL    |       |

| start_time          | datetime    | YES  |     | NULL    |       |

| current_interest    | bigint      | YES  |     | NULL    |       |

| amount_withdrawable | bigint      | YES  |     | NULL    |       |

| expected_interest   | bigint      | YES  |     | NULL    |       |

| amount_onmaturity   | bigint      | YES  |     | NULL    |       |

| end_time            | datetime    | YES  |     | NULL    |       |

