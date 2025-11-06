from ldap3 import Server, Connection, MOCK_SYNC, ALL

# mock LDAP server
server = Server('mock_ldap', get_info=ALL)
conn = Connection(
    server,
    user='cn=admin,dc=echelon,dc=com',
    password='secret',
    client_strategy=MOCK_SYNC
)
conn.bind()

# add sample entries
conn.strategy.add_entry(
    'cn=Jane Doe,ou=users,dc=echelon,dc=com',
    {
        'objectClass': ['inetOrgPerson'],
        'mail': ['jane.doe@echelon.com'],
        'departmentNumber': ['Finance']
    }
)

conn.strategy.add_entry(
    'cn=Mark Smith,ou=users,dc=echelon,dc=com',
    {
        'objectClass': ['inetOrgPerson'],
        'mail': ['mark.smith@echelon.com'],
        'departmentNumber': ['Engineering']
    }
)

print("=== LDAP Directory Dump ===")
results = conn.extend.standard.paged_search(
    search_base='dc=echelon,dc=com',
    search_filter='(objectClass=*)',
    attributes=['mail', 'departmentNumber'],
    paged_size=5,
    generator=False
)
for entry in results:
    print(entry)
