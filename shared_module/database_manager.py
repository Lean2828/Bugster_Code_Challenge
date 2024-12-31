from pymongo import MongoClient, UpdateOne
from pymongo.collection import Collection
from models.event import Event
from models.story import Story
from logging_config import logger
from typing import Optional, List

class DatabaseManager:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def close(self):
        if self._client:
            self._client.close()
            self._client = None        

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]

    def create_indexes(self):
        """
        Crea índices en las colecciones para mejorar el rendimiento de las consultas.
        """
        try:
            events_collection = self.get_collection("events")
            events_collection.create_index("properties.distinct_id")
            events_collection.create_index("properties.session_id")
            events_collection.create_index("timestamp")
            logger.info("Índices creados en la colección de eventos.")
        except Exception as e:
            logger.error(f"Error creando índices: {str(e)}", exc_info=True)
            raise

    def bulk_save_events(self, events: List[Event]):
        """
        Guarda o actualiza una lista de eventos en la base de datos utilizando una operación masiva.

        Args:
            events (List[Event]): Lista de instancias de la clase Event.
        """
        events_collection = self.get_collection("events")
        bulk_operations = []

        try:
            for event in events:
                filter_key = {
                    "properties.distinct_id": event.properties.distinct_id,
                    "properties.session_id": event.properties.session_id,
                    "timestamp": event.timestamp,
                }

                event_json = event.to_json()

                bulk_operations.append(
                    UpdateOne(filter_key, {"$set": event_json}, upsert=True)
                )

            if bulk_operations:
                events_collection.bulk_write(bulk_operations)

        except Exception as e:
            logger.error(f"Error ejecutando bulk_save_events: {str(e)}", exc_info=True)
            raise


        if bulk_operations:
            try:
                events_collection.bulk_write(bulk_operations)
                logger.info(f"Se guardaron {len(bulk_operations)} eventos.")
            except Exception as e:
                logger.error(f"Error guardando eventos en bulk: {str(e)}", exc_info=True)
                raise

    def bulk_upsert_sessions(self, sessions: List[dict]):
        """
        Inserta o actualiza masivamente las sesiones en MongoDB.
        """
        sessions_collection = self.get_collection("sessions")
        bulk_operations = []

        for session in sessions:
            bulk_operations.append(
                UpdateOne(
                    {"distinct_id": session["distinct_id"]},
                    {"$addToSet": {"sessions": {"$each": session["sessions"]}}},
                    upsert=True,
                )
            )

        if bulk_operations:
            try:
                sessions_collection.bulk_write(bulk_operations)
                logger.info(f"Se actualizaron {len(bulk_operations)} sesiones.")
            except Exception as e:
                logger.error(f"Error actualizando sesiones en bulk: {str(e)}", exc_info=True)
                raise

        
    def get_events_by_sessions(self, session_ids: List[str]) -> List[dict]:
        """
        Obtiene todos los eventos asociados a una lista de session_id.

        Args:
            session_ids (List[str]): Lista de session_id.
            events_collection (Collection): Colección de eventos.

        Returns:
            List[dict]: Lista de eventos.
        """
        
        events_collection = self.get_collection("events")
        
        return list(events_collection.find({"properties.session_id": {"$in": session_ids}}))

   
    def get_all_stories(self, session_id: Optional[str] = None) -> List[Story]:
        """
        Obtiene historias con o sin filtro por `session_id` y las convierte a instancias de `Story`.

        Args:
            session_id (Optional[str]): ID de sesión para filtrar historias.

        Returns:
            List[Story]: Lista de instancias de `Story`.
        """
        stories_collection = self.get_collection("stories")
        query = {"session_id": session_id} if session_id else {}
        return list(stories_collection.find(query, {"_id": 0}))
        

    def get_stories_by_distinct_id(self, distinct_id: str) -> List[dict]:
        """
        Obtiene historias asociadas a un `distinct_id`.

        Args:
            distinct_id (str): ID único del usuario.

        Returns:
            List[dict]: Lista de historias.
        """
        stories_collection = self.get_collection("stories")
        story_id = f"story-{distinct_id}"  # Formar el ID de la historia
        query = {"id": story_id}

        print
        # Excluir el campo `_id` de los resultados
        return list(stories_collection.find(query, {"_id": 0}))

    def get_distinct_id_by_session_id(self, session_id: str) -> Optional[str]:
        """
        Obtiene el `distinct_id` asociado a un `session_id` desde la tabla `sessions`.

        Args:
            session_id (str): ID de sesión.

        Returns:
            Optional[str]: ID único del usuario asociado, o None si no se encuentra.
        """
        sessions_collection = self.get_collection("sessions")
        result = sessions_collection.find_one(
            {"sessions": session_id},  # Filtro: busca el `session_id` dentro del campo `sessions`
            {"distinct_id": 1, "_id": 0}  # Proyección: incluye `distinct_id` y excluye `_id`
        )
        return result["distinct_id"] if result else None

    def bulk_upsert_stories(self, stories: List[Story]):
        """
        Inserta o actualiza masivamente las historias en la base de datos.

        Args:
            stories (List[Story]): Lista de historias.
        """
        stories_collection = self.get_collection("stories")
        bulk_operations = []
        for story in stories:
            bulk_operations.append(
                UpdateOne(
                    {"id": story.id},
                    {"$set": {"session_id": story.session_id, **story.model_dump()}},
                    upsert=True,
                )
            )

        if bulk_operations:
            try:
                stories_collection.bulk_write(bulk_operations)
                logger.info(f"Se guardaron/actualizaron {len(bulk_operations)} historias.")
            except Exception as e:
                logger.error(f"Error ejecutando bulk_upsert_stories: {str(e)}", exc_info=True)
                raise
            
    def get_stories_by_session_id(self, session_id: str) -> List[dict]:
        """
        Obtiene historias asociadas a un `session_id`.

        Args:
            session_id (str): ID de la sesión.

        Returns:
            List[dict]: Lista de historias asociadas al session_id.
        """
        stories_collection = self.get_collection("stories")
        query = {"session_id": session_id}
        return list(stories_collection.find(query, {"_id": 0}))
            
    def get_stories_by_story_id(self, story_id: str) -> List[dict]:
        """
        Obtiene historias asociadas a un `story_id`.

        Args:
            story_id (str): ID de la sesión.

        Returns:
            List[dict]: Lista de historias asociadas al story_id.
        """
        stories_collection = self.get_collection("stories")
        query = {"id": story_id}
        return list(stories_collection.find(query, {"_id": 0}))
            
