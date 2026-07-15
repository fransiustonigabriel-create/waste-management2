from assistant.knowledge import KNOWLEDGE_BASE


def load_all_knowledge():
    """
    Mengembalikan seluruh knowledge yang tersedia.
    """

    return KNOWLEDGE_BASE


def load_by_name(name):
    """
    Mengambil knowledge berdasarkan nama.
    """

    return KNOWLEDGE_BASE.get(name)