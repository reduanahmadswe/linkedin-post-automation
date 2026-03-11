import os
import logging
import requests
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv()

LINKEDIN_API_URL = "https://api.linkedin.com/v2/ugcPosts"

logger = logging.getLogger(__name__)


def get_linkedin_credentials() -> tuple[str, str]:
    """
    Load LinkedIn credentials from environment variables.
    Returns (access_token, person_urn) tuple.
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN", "").strip()
    person_urn = os.getenv("LINKEDIN_PERSON_URN", "").strip()
    return access_token, person_urn


def publish_to_linkedin(post_text: str) -> dict:
    """
    Publish a post to LinkedIn using the UGC API.
    
    Args:
        post_text: The text content to publish.
        
    Returns:
        dict with 'success' (bool) and 'message' or 'error' keys.
    """
    # Load credentials
    access_token, person_urn = get_linkedin_credentials()
    
    # Debug logging - token loaded status
    if access_token:
        logger.info("LINKEDIN_ACCESS_TOKEN loaded successfully (length: %d)", len(access_token))
    else:
        logger.error("LINKEDIN_ACCESS_TOKEN is missing or empty!")
        return {
            "success": False,
            "error": "LinkedIn access token is missing. Please set LINKEDIN_ACCESS_TOKEN in .env file."
        }
    
    if not person_urn:
        logger.error("LINKEDIN_PERSON_URN is missing or empty!")
        return {
            "success": False,
            "error": "LinkedIn person URN is missing. Please set LINKEDIN_PERSON_URN in .env file."
        }
    
    logger.info("LINKEDIN_PERSON_URN loaded: %s", person_urn)
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    # Construct UGC API payload
    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    logger.debug("Sending request to LinkedIn API: %s", LINKEDIN_API_URL)
    
    try:
        response = requests.post(LINKEDIN_API_URL, headers=headers, json=payload, timeout=30)
        
        # Debug logging - response details
        logger.info("LinkedIn API response status code: %d", response.status_code)
        logger.debug("LinkedIn API response text: %s", response.text)
        
        if response.status_code == 201:
            logger.info("Post published successfully to LinkedIn!")
            return {
                "success": True,
                "message": "Post published successfully to LinkedIn.",
                "response": response.json() if response.text else {}
            }
        else:
            logger.error("LinkedIn API error: %s", response.text)
            return {
                "success": False,
                "error": f"LinkedIn API error (status {response.status_code}): {response.text}"
            }
            
    except requests.exceptions.Timeout:
        logger.error("LinkedIn API request timed out")
        return {
            "success": False,
            "error": "Request to LinkedIn API timed out."
        }
    except requests.exceptions.RequestException as e:
        logger.error("LinkedIn API request failed: %s", str(e))
        return {
            "success": False,
            "error": f"Request to LinkedIn API failed: {str(e)}"
        }


def publish_post(content: str) -> bool:
    """
    Legacy wrapper for backward compatibility.
    Use publish_to_linkedin() for new code.
    """
    result = publish_to_linkedin(content)
    return result.get("success", False)
