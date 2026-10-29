# Understanding ChatGPT Parameters

> **Source / origin note.** External course material — *not* Murdoch. "AI for Marketers" reference from the Galileo University + Davidson College course (Course 1, *Intro to AI for Digital Marketing*). Text reproduced verbatim for study reference; chat exchanges shown as **You / ChatGPT** blocks.
>
> *Note: these are conceptual descriptions of generation parameters (temperature, top-p, penalties, max tokens, stop sequences). In ChatGPT's chat interface you cannot literally set these as numbers — the guide demonstrates referencing them inside the prompt text. they are genuine API generation parameters, and behaviour and availability differ across models/years.*

---

The parameters in the context of ChatGPT refer to the configurable settings that can be adjusted to influence the model's behavior and the output it generates. These parameters allow users to customize the AI's responses based on their preferences, style, and requirements. Here are some key parameters that might be relevant:

---

## Temperature

Temperature is a parameter that controls the randomness of the generated output. The temperature ranges from **0 to 1**.

- A **higher** temperature (e.g., 0.8) makes the responses more creative and varied.
- A **lower** temperature (e.g., 0.2) produces more focused and deterministic responses.

### Example

**Prompt without the parameter:** *"Write a 160-character meta description for the blog post 'Top 10 tips for successful blogging: Boost your online presence and engage with your audience.'"*

> **You:** Write a 160-character meta description for the blog post "Top 10 tips for successful blogging: Boost your online presence and engage with your audience"
>
> **ChatGPT:** "Unlock the secrets to successful blogging! Learn 10 essential tips to enhance your online presence and captivate your audience effectively."

**Prompt with the parameter of temperature:** *Now, write a 160-character meta description for the blog post "Top 10 tips for successful blogging: Boost your online presence and engage with your audience" **using a "temperature" value of 1 in the output**.*

> **You:** Now, write a 160-character meta description for the blog post "Top 10 tips for successful blogging: Boost your online presence and engage with your audience" using a "temperature" value of 1 in the output.
>
> **ChatGPT:** "Discover the hottest tips for successful blogging! Elevate your online presence and connect with your audience like never before. 🔥"

---

## Diversity_Penalty

This parameter penalizes the repetition of words or phrases, making the model more likely to generate responses containing a variety of different words and concepts.

It is measured on a scale from **0 to 2**, with higher values resulting in more diverse outputs.

- **Low diversity (0):** No penalty is applied; repetitive phrases are allowed.
- **Medium diversity (1):** Balanced diversity and coherence.
- **High diversity (2):** Maximum diversity, which may affect coherence.

### Example

**Prompt without parameter:** *"Product Description for a cotton t-shirt."*

> **You:** Product Description for a cotton t-shirt
>
> **ChatGPT:** Introducing our premium cotton t-shirt, a staple for every wardrobe. Made from soft, breathable cotton, it offers ultimate comfort and versatility. Whether you're lounging at home or out for a casual stroll, this t-shirt keeps you cool and stylish all day long. With a classic crew neck and a relaxed fit, it's perfect for layering or wearing on its own. Available in a variety of vibrant colors, this t-shirt is a must-have for effortless everyday style. Upgrade your basics with our comfortable and durable cotton t-shirt today!
>
> *(Note: the word "t-shirt" repeats several times — highlighted in the original to show the lack of diversity penalty.)*

**Prompt with the parameter:** *"Using the Diverse_penalty (1) in our conversation: write a Product Description for a cotton t-shirt."*

> **You:** Using the Diverse_penalty (1) in our conversation: write a Product Description for a cotton t-shirt
>
> **ChatGPT:** Introducing our diverse collection of cotton t-shirts, designed for all shapes, sizes, and styles. Crafted from premium-quality cotton, these tees offer unbeatable comfort and versatility. Whether you're lounging at home or hitting the streets, our t-shirts ensure you stay cool and stylish all day long. With a range of inclusive sizes and a variety of vibrant colors, there's something for everyone in our collection. Elevate your wardrobe with our comfortable and durable cotton t-shirts, celebrating diversity and effortless style.

---

## Max Tokens

Tokens are text chunks that can be as short as a character or as long as a word, depending on the language. This parameter determines the maximum length of the generated text.

By setting a limit, you can control how much the AI says, ensuring it doesn't provide excessively long responses.

### Example

**Prompt without parameter:** *"What is digital marketing?"*

> **You:** What is digital marketing?
>
> **ChatGPT:** Digital marketing refers to the use of online channels, platforms, and technologies to promote products, services, or brands to consumers and businesses. It encompasses a wide range of tactics and strategies, including search engine optimization (SEO), content marketing, social media marketing, email marketing, pay-per-click (PPC) advertising, and more. Digital marketing aims to reach target audiences where they spend their time online, engaging them with relevant content and messages to drive desired actions, such as website visits, leads, sales, or brand awareness. It offers the ability to track and measure campaign performance in real-time, allowing for optimization and refinement based on data-driven insights.

**Prompt with the parameter:** *"Language model, max_tokens = 50: What is digital marketing?"*

> **You:** Language model, max_tokens=50: what is digital marketing?
>
> **ChatGPT:** Digital marketing is the promotion of products or services using online channels such as social media, email, and search engines. It aims to reach target audiences and drive desired actions like website visits or sales.

---

## Stop Sequences

Stop sequences are specific strings of text that prompt the model to halt its generation process when encountered. This functionality serves to control output length or guide the model to cease at logical endpoints.

**Example:** In a formal letter, employing "Yours sincerely," as a stop sequence ensures the AI stops generating text beyond the appropriate conclusion of the letter.

---

## Top P

The 'Top P' parameter, also referred to as nucleus sampling, dynamically selects the number of words considered in the model's predictions at each step. Lower values, such as 0.5, yield focused outputs, while higher values, like 0.9, result in more diverse outputs.

**Example:** When developing an AI for composing poems and desiring a broad vocabulary and stylistic variety, opting for a higher 'Top P' value is advisable. For instance, the prompt could be: *"Create a poem capturing the beauty of autumn."*

---

## Here are more examples

**1. Tone**
- *Instruction:* "Write a promotional tweet for our new beauty product using a **playful tone**."
- *Result:* "Want skin softer than a unicorn caressed by a rainbow? Try our magical cream today! 🦄✨"

**2. Format**
- *Instruction:* "Create a follow-up email for customers who abandoned their shopping cart **in list format**."
- *Result:*
  - Subject: Don't Forget Your Items!
  - Organic Cotton T-Shirt
  - Slim-Fit Jeans
  - Sneakers

**3. Audience**
- *Instruction:* "Write a blog post about marketing strategies **tailored to small business owners**."
- *Result:* "5 Practical Tips to Boost Your Business with Digital Marketing"

**4. Maximum Length**
- *Instruction:* "Create a memorable slogan for a gourmet coffee brand that is **no longer than 10 words**."
- *Result:* "Awaken your senses with every sip: Aromatic Coffee, Unforgettable Flavor."

**5. Stop Sequence**
- *Instruction:* "Generate ideas for a 30-second TV ad for a new perfume, **stopping before mentioning the actual product name**."
- *Result:* "Images of a blooming garden, intense gazes, whispered secrets. Eternal Perfume: Find your passion."

**6. Frequency Penalty**
- *Instruction:* "Describe the benefits of our loyalty program **without repeating the word 'rewards' more than once**, emphasizing its value."
- *Result:* "Our loyalty program offers exclusive advantages like discounts, early access to products, and special events."

**7. Presence Penalty**
- *Instruction:* "Explain how cryptography works **without using the word 'key'** in your response, focusing on its security features."
- *Result:* "Cryptography ensures data confidentiality, integrity, and authenticity through mathematical techniques and algorithms."

**8. Audience Description**
- *Instruction:* "Please generate marketing copy targeting a young adult audience (aged 18-30) for a new energy drink. Emphasize the drink's ability to boost energy levels during workouts and late-night study sessions. **Set the temperature to 0.7, limit the maximum tokens to 100, apply a frequency penalty of 0.6, and stop generating text after three sentences.**"
- *Result:* "Introducing [Product Name], the ultimate companion for the modern young adult! Are you burning the midnight oil or pushing your limits at the gym? Say goodbye to fatigue and hello to boundless energy with our specially crafted formula. With [Product Name], you'll power through workouts and late-night study sessions with ease."

**9. Brand Persona**
- *Instruction:* "Develop a social media post promoting a luxury fashion brand. The brand persona should exude sophistication and exclusivity, targeting affluent individuals aged 25-45. **Set the temperature to 0.8, limit the maximum tokens to 120, apply a frequency penalty of 0.5, and stop generating text after two sentences.**"
- *Result:* "Elevate your style to new heights with [Brand Name]. Immerse yourself in the world of luxury and sophistication. Our timeless pieces are crafted for those who appreciate the finer things in life."

**10. Emotional Appeal**
- *Instruction:* "Create a tagline for a travel agency aiming to evoke a sense of adventure and wanderlust among its audience. **Set the temperature to 0.6, limit the maximum tokens to 80, apply a frequency penalty of 0.7, and stop generating text after one sentence.**"
- *Result:* "Escape. Explore. Experience. Your journey begins with us."

**11. Call to Action (CTA)**
- *Instruction:* "Write a blog post encouraging readers to sign up for a cooking class offered by a culinary school. Include a compelling call to action urging readers to register for a class. **Set the temperature to 0.7, limit the maximum tokens to 150, apply a frequency penalty of 0.6, and stop generating text after four sentences.**"
- *Result:* "Ready to unleash your inner chef? Join us at [Culinary School Name] and embark on a culinary journey like no other! From mastering the basics to perfecting gourmet dishes, our classes cater to all skill levels. Don't just dream of becoming a culinary whiz – make it a reality!"

---

## Do you want to know more about?

- A Complete Guide to Prompt Engineering: Marketer's Edition
- A Marketer's Guide to Mastering Prompt Engineering
- Prompt Engineering: A Guide for Marketers and Content Creators

**Source:** Adapted from Budau, A. (2023). *My Secret ChatGPT — Use ChatGPT like a Pro: Discover Parameters and Unlock AI Writing Secrets.* https://uxplanet.org/use-chatgpt-like-a-pro-discover-parameters-and-unlock-ai-writing-secrets-8f68a342bdea
