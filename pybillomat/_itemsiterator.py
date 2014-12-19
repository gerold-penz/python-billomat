#!/usr/bin/env python
# coding: utf-8


class ItemsIterator(object):
    """
    ItemsIterator

    Base class for ClientsIterator, RecurringsIterator, ...
    """

    items = None


    def search(self):
        raise NotImplementedError()


    def load_page(self, page):
        raise NotImplementedError()


    def __len__(self):
        """
        Returns the count of found recurrings
        """

        return self.items.total or 0


    def __iter__(self):
        """
        Iterate over all found items
        """

        if not self.items.pages:
            return

        for page in range(1, self.items.pages + 1):
            if not self.items.page == page:
                self.load_page(page = page)
            for item in self.items:
                yield item


    def __getitem__(self, key):
        """
        Returns the requested recurring from the pool of found recurrings
        """

        # List-Ids
        all_list_ids = range(len(self))
        requested_list_ids = all_list_ids[key]
        is_list = isinstance(requested_list_ids, list)
        if not is_list:
            requested_list_ids = [requested_list_ids]
        assert isinstance(requested_list_ids, list)

        result = []

        for list_id in requested_list_ids:

            # In welcher Seite befindet sich die gewünschte ID?
            for page_nr in range(1, self.items.pages + 1):
                max_list_id = (page_nr * self.items.per_page) - 1
                if list_id <= max_list_id:
                    page = page_nr
                    break
            else:
                raise AssertionError()

            # Load page if neccessary
            if not self.items.page == page:
                self.load_page(page = page)

            # Add equested invoice-object to result
            list_id_in_page = list_id - ((page - 1) * self.items.per_page)
            result.append(self.items[list_id_in_page])

        if is_list:
            return result
        else:
            return result[0]
