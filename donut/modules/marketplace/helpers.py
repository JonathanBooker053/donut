import flask
import sqlalchemy

def get_marketplace_items_list_data(fields=None, attrs={}):
    """
    Queries the database and returns list of member data constrained by the 
    specified attributes.

    Arguments:
        fields: The fields to return. If None specified, then default_fields
                are used.
        attrs:  The attributes of the members to filter for.
    Returns:
        result: The fields and corresponding values of members with desired
                attributes. In the form of a list of dicts with key:value of 
                columnname:columnvalue.
    """
    all_returnable_fields = ["item_id", "cat_id", "user_id", "item_title", "item_details",
         "item_images", "item_condition", "item_price", "item_timestamp",
         "item_active", "textbook_id", "textbook_isbn", "textbook_version"]
    default_fields = ["item_id", "cat_id", ]
    if fields == None:
        fields = default_fields
    else:
        if any(f not in all_returnable_fields for f in fields):
            return "Invalid field"

    # Build the SELECT and FROM clauses
    s = sqlalchemy.sql.select(fields).select_from(sqlalchemy.text("marketplace_items"))
    
    # Build the WHERE clause 
    for key, value in attrs.items():
        s = s.where(sqlalchemy.text(key + "= :" + key))

    # Execute the query
    result = flask.g.db.execute(s, attrs).fetchall()
    
    # Return the row in the form of a of dict
    result = { f:t for f,t in zip(fields, result) }
    return result
