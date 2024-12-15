import os
import logging
import requests
import base64
from typing import Union, List, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

class Sinch:
    def __init__(self):
        logger.info("Initializing Sinch client")
        try:
            self.api_key = os.getenv("SINCH_API_KEY_ID")
            self.api_secret = os.getenv("SINCH_API_KEY_SECRET")
            self.project_id = os.getenv("SINCH_API_PROJECT_ID")
            self.app_id = os.getenv("SINCH_APP_ID")
            self.base_url = "https://eu.conversation.api.sinch.com/v1"

            # Generate access token
            self.access_token = self._generate_access_token()

            logger.debug("Sinch REST client initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize Sinch REST client: %s", str(e))
            raise

    def _generate_access_token(self) -> str:
        """
        Generate Basic Auth token from API key and secret

        Returns:
            str: Base64 encoded access token
        """
        data = f"{self.api_key}:{self.api_secret}"
        encoded_bytes = base64.b64encode(data.encode("utf-8"))
        return str(encoded_bytes, "utf-8")

    def send_rcs(self,
                to: Union[str, List[str]],
                message: str,
                delivery_report: str = "none") -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Send RCS using Sinch Conversation API

        Args:
            to (str or list): Phone number(s) to send RCS to
            message (str): Message content
            delivery_report (str, optional): Delivery report type. Defaults to "none"

        Returns:
            dict or list: Response(s) from Sinch Conversation API
        """
        if not isinstance(message, str):
            message = str(message)

        # Convert single number to list
        to_numbers = [to] if isinstance(to, str) else to

        # Clean phone numbers and ensure they're in E.164 format
        to_numbers = [
            str(num).strip().replace(' ', '')
            for num in to_numbers
        ]

        logger.info("Sending RCS to %d recipient(s)", len(to_numbers))
        logger.info(
            "RCS details - Recipients: %s, Message length: %d",
            repr(to_numbers),
            len(message)
        )

        url = f"{self.base_url}/projects/{self.project_id}/messages:send"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.access_token}"
        }

        responses = []
        try:
            for recipient_number in to_numbers:
                payload = {
                    "app_id": self.app_id,
                    "recipient": {
                        "identified_by": {
                            "channel_identities": [
                                {
                                    "identity": recipient_number,
                                    "channel": "RCS"
                                }
                            ]
                        }
                    },
                    "message": {
                        "text_message": {
                            "text": message
                        }
                    }
                }

                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()  # Raise exception for non-200 status codes

                response_data = response.json()
                responses.append(response_data)

                logger.info("RCS sent successfully to %s", recipient_number)
                logger.debug("Sinch API response: %s", repr(response_data))

            return responses[0] if len(responses) == 1 else responses

        except requests.exceptions.RequestException as e:
            logger.error("Failed to send RCS batch: %s", str(e))
            raise
