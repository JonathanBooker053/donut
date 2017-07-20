import flask
import json

from donut.modules.marketplace import blueprint, helpers

@blueprint.route('/marketplace')
def marketplace():
    """Display marketplace page."""

    return helpers.render_top_marketplace_bar('marketplace.html', cat_id=0)
    # cat_id = 0 indicates "all categories", which is the default


@blueprint.route('/marketplace/view')
def category():
    """Display all results in that category, with no query."""

    category_id = flask.request.args["cat"]

    return helpers.render_top_marketplace_bar('search.html', cat_id=category_id)


@blueprint.route('/marketplace/search')
def query():
    """Displays all results for the query in category category_id, which can be
       'all' if no category is selected."""

    category_id = flask.request.args["cat"]
    query = flask.request.args["q"]

    fields = ["item_title", "item_price", "user_id", "item_timestamp"]
    # Create a dict of the passed in attributes which are filterable
    filterable_attrs = ["item_id", "cat_id", "user_id", "item_title",
            "item_details", "item_images", "item_condition",
            "item_price", "item_timestamp", "item_active",
            "textbook_id", "textbook_isbn", "textbook_version"]
    attrs = { tup:flask.request.args[tup]
            for tup in flask.request.args if tup in filterable_attrs }
    if category_id == "all":
        category_id = 0

    # now, the category id had better be a number
    try:
        cat_id_num = int(category_id)
        datadump = helpers.get_marketplace_items_list_data(fields=fields, attrs=attrs)
        datalist = []
        # make datadump a 2d list instead of a dict
        for data in datadump:
            templist = []
            for field in fields:
                templist.append(data[field])
            datalist.append(templist)

        return helpers.render_top_marketplace_bar('search.html', datalist=datalist, cat_id=cat_id_num, headers=fields)

    except ValueError:
        # not a number? something's wrong
        return flask.render_template('404.html')


@blueprint.route('/marketplace/sell')
def sell():
    return helpers.render_top_marketplace_bar('sell.html')


@blueprint.route('/1/marketplace_items')
def get_marketplace_items_list():
    """GET /1/marketplace_items/"""

    # Create a dict of the passed in attributes which are filterable
    filterable_attrs = ["item_id", "cat_id", "user_id", "item_title",
            "item_details", "item_images", "item_condition",
            "item_price", "item_timestamp", "item_active",
            "textbook_id", "textbook_isbn", "textbook_version"]
    attrs = { tup:flask.request.args[tup]
            for tup in flask.request.args if tup in filterable_attrs }
    # Get the fields to return if they were passed in
    fields = None
    if "fields" in flask.request.args:
        fields = [f.strip() for f in flask.request.args["fields"].split(',')]

    return json.dumps(helpers.get_marketplace_items_list_data(fields=fields, attrs=attrs))
