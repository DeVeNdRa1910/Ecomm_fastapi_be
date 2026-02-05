from fastapi import APIRouter, Depends, Request
from app.services.get_current_user import get_current_user_by_token
from app.configs.ENV import ENV_Config
from app.schemas.stripe_schema import (
    StripeSessionResponse,
    StripeCreateSession
)
import stripe

router = APIRouter()

stripe.api_key = ENV_Config.STRIPE_SECRET_KEY

@router.post("/create-checkout-session", dependencies=[Depends(get_current_user_by_token)], response_model=StripeSessionResponse, status_code=201)
async def create_checkout(payload: StripeCreateSession):
    
    product_list = []
    
    for product in payload.products:
        product_list.append({
            "price_data":{
                "currency": "inr",
                "product_data": {"name": product.name},
                "unit_amount": product.price*100
            },
            "quantity": product.quantity
        })
    
    session = stripe.checkout.session.create(
        payment_method_types = ["card"],
        line_items = product_list,
        mode="payment",
        success_url=ENV_Config.STRIPE_PAYMENT_SUCCESS_URL,
        cancel_url=ENV_Config.STRIPE_PAYMENT_FAILED_URL
    )
    
    return StripeSessionResponse( url=session.url )

@router.post("/webhook", status_code=201)
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = ENV_Config.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]
        return {"status": "success", "id": session["id"]}
        
    except stripe.error.SignatureVerificationError as e:
        return {"status": f"invalid signature: {e}"}